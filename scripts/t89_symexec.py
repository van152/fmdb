#!/usr/bin/env python3
"""t89_symexec — t9_read(0x14105d510) 的符号执行器,产出条目字段网格。

思路:不猜循环结构,直接把读取函数当程序跑。
  - 输入流 = body 字节(每读 N 字节取流中下一个 N)
  - 寄存器/栈槽用 dict 建模;只建模影响控制流的量
  - `call [rax+0x28]` 读流:宽度取紧邻 `mov r8d, W`,目标取 `lea rdx, DST`
  - 已知辅助函数按语义建模(HELPERS),未知记 gap 后继续
  - 版本号来自 word ptr [r14+0x588],由参数给定

用法:
  py -V:3.12 -I -B scripts/t89_symexec.py --trace client 96
  py -V:3.12 -I -B scripts/t89_symexec.py --validate
  py -V:3.12 -I -B scripts/t89_symexec.py --selftest
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
ENTRY = 0x14105D510
MAX_STEPS = 500_000
CALL_R28 = "call qword ptr [rax + 0x28]"


def _mod(name: str, rel: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / rel)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


REG64 = ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp",
         "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]
ALIAS = {"eax": ("rax", 4), "ebx": ("rbx", 4), "ecx": ("rcx", 4), "edx": ("rdx", 4),
         "esi": ("rsi", 4), "edi": ("rdi", 4), "ebp": ("rbp", 4), "esp": ("rsp", 4),
         "r8d": ("r8", 4), "r9d": ("r9", 4), "r10d": ("r10", 4), "r11d": ("r11", 4),
         "r12d": ("r12", 4), "r13d": ("r13", 4), "r14d": ("r14", 4), "r15d": ("r15", 4),
         "ax": ("rax", 2), "bx": ("rbx", 2), "cx": ("rcx", 2), "dx": ("rdx", 2),
         "si": ("rsi", 2), "di": ("rdi", 2), "bp": ("rbp", 2),
         "r8w": ("r8", 2), "r9w": ("r9", 2), "r12w": ("r12", 2), "r13w": ("r13", 2),
         "al": ("rax", 1), "bl": ("rbx", 1), "cl": ("rcx", 1), "dl": ("rdx", 1),
         "sil": ("rsi", 1), "dil": ("rdi", 1), "r12b": ("r12", 1), "r13b": ("r13", 1),
         "r14b": ("r14", 1), "r15b": ("r15", 1)}


def canon(reg: str) -> str:
    r = reg.strip()
    if r in REG64:
        return r
    if r in ALIAS:
        return ALIAS[r][0]
    return r


def _ops(op: str) -> list[str]:
    out, cur, br = [], "", 0
    for ch in op:
        if ch == "[":
            br += 1
        elif ch == "]":
            br -= 1
        if ch == "," and br == 0:
            out.append(cur.strip())
            cur = ""
        else:
            cur += ch
    if cur.strip():
        out.append(cur.strip())
    return out


def parse_mem(s: str):
    """'[rsi + 0x488]' / 'qword ptr [rbp - 0x40]' / '[rsp + rcx*4 + 8]'
    -> (base, idx, scale, disp)。"""
    t0 = s.strip()
    m = re.match(r"^(?:qword|dword|word|byte) ptr \[(.+)\]$", t0)
    if m:
        inner = m.group(1)
    elif t0.startswith("[") and t0.endswith("]"):
        inner = t0[1:-1]
    else:
        return None
    toks = [t.strip() for t in inner.split("+")]
    base = idx = None
    scale = 1
    disp = 0
    for t in toks:
        t2 = t.replace("-", "+-")
        for part in [p.strip() for p in t2.split("+")]:
            if not part:
                continue
            mm = re.match(r"^(\w+)\*(\d+)$", part)
            if mm:
                idx, scale = mm.group(1), int(mm.group(2))
                continue
            if part in REG64 or part in ALIAS:
                base = canon(part)
                continue
            try:
                disp += int(part, 0)
            except ValueError:
                return None
    return (base, idx, scale, disp)


class Machine:
    def __init__(self, body: bytes, version: int, ins: list[dict]):
        self.body = body
        self.pos = 0
        self.version = version
        self.ins = ins
        self.pc = 0
        self.frames: list[tuple[list[dict], int]] = []
        self.depth = 0
        self._cache: dict[int, list[dict]] = {ENTRY: ins}
        self.regs = {r: 0 for r in REG64}
        self.regs["rsp"] = 0x7FF000
        self.regs["rbp"] = 0x7FF000
        self.mem: dict[int, int] = {}
        self.fields: list[dict] = []
        self.gaps: list[str] = []
        self.calls: list[str] = []
        self.steps = 0
        self.objbase = 0x100000       # rsi = this (NATION_T9)
        self.stream = 0x900000        # r13 -> 读流对象
        self.regs["rsi"] = self.objbase
        self.regs["r14"] = 0x200000   # r9 = 版本宿主
        self.regs["r13"] = self.stream
        self.mem[self.regs["r14"] + 0x588] = version
        self.mem[self.stream] = 0x910000
        # 栈参数:[rsp+0x140] = 单字节标志(client=1)
        self.mem[self.regs["rsp"] + 0x140] = 1
        self.zf = self.sf = self.of = self.cf = False
        self.last_r8d = None
        self.last_dst = None
        self.rdx_desc: str | None = None
        self.ret_flag: list[bool] = []

    # --- 内存 ---
    def addr(self, expr: str) -> int | None:
        p = parse_mem(expr)
        if p is None:
            return None
        base, idx, scale, disp = p
        a = 0
        if base:
            a += self.regs.get(base, 0)
        if idx:
            a += self.regs.get(idx, 0) * scale
        return a + disp

    def load(self, expr: str, size: int = 8):
        a = self.addr(expr)
        if a is None:
            return None
        if a == self.stream or a == 0xA00000:
            return self.stream
        return self.mem.get(a, 0)

    def store(self, expr: str, val: int):
        a = self.addr(expr)
        if a is None:
            return
        self.mem[a] = val

    # --- 读流 ---
    def read_stream(self, width: int, dst: str | None, va: int):
        if self.pos + width > len(self.body):
            self.gaps.append(f"overflow va=0x{va:x} w={width} pos={self.pos}")
            return None
        raw = self.body[self.pos:self.pos + width]
        self.fields.append({"off": self.pos, "w": width, "dst": dst,
                            "va": f"0x{va:x}", "raw": raw.hex()})
        self.pos += width
        return int.from_bytes(raw, "little", signed=(width <= 4))

    def resolve(self, va: int) -> int:
        """跟随 jmp thunk,拿到真正函数体起点。"""
        for _ in range(6):
            D = _mod("d", "scripts/t89_pe.py")
            try:
                code = D.disasm(va, 8)
            except Exception:
                return va
            if not code:
                return va
            x = code[0]
            if x["mn"] == "jmp" and re.match(r"^0x[0-9a-f]+$", x["op"]):
                va = int(x["op"], 16)
                continue
            return va
        return va

    def disasm_at(self, va: int, maxlen: int = 0x600) -> list[dict] | None:
        """按需反汇编 VA 处的函数(直到 ret 为止)。"""
        va = self.resolve(va)
        if va in self._cache:
            return self._cache[va]
        D = _mod("d", "scripts/t89_pe.py")
        try:
            code = D.disasm(va, maxlen)
        except Exception:
            return None
        if not code:
            return None
        out = []
        for x in code:
            out.append(x)
            if x["mn"] == "ret":
                break
        self._cache[va] = out
        return out

    def enter(self, va: int) -> bool:
        code = self.disasm_at(va)
        if code is None:
            return False
        self.frames.append((self.ins, self.pc))
        self.ins, self.pc = code, 0
        self.depth += 1
        return True

    def call_enter(self, va: int) -> bool:
        if not self.enter(va):
            return False
        self.ret_flag.append(True)
        return True
    def run(self) -> dict:
        ins = self.ins
        while 0 <= self.pc < len(self.ins):
            self.steps += 1
            if self.steps > MAX_STEPS:
                self.gaps.append("step budget exhausted")
                break
            ins = self.ins
            x = ins[self.pc]
            va, t = x["va"], x["text"]
            if not t:
                self.pc += 1
                continue
            mn = t.split()[0]
            ops = _ops(t[len(mn):].strip())

            if mn == "ret":
                if self.frames:
                    self.ins, self.pc = self.frames.pop()
                    self.depth -= 1
                    self.pc += 1
                    if self.ret_flag:
                        # 读取辅助函数返回“成功”
                        self.regs["rax"] = 1 if self.ret_flag.pop() else 0
                    continue
                break
            if mn in ("int3", "hlt"):
                break
            if mn == "jmp":
                tgt = int(ops[0], 16)
                nxt = self._jump(tgt)
                if nxt is None:
                    break
                continue
            if mn in ("jne", "je", "jl", "jle", "jg", "jge", "jb", "jbe",
                      "ja", "jae", "js", "jns", "jrcxz"):
                tgt = int(ops[0], 16)
                take = self._cond(mn)
                if take:
                    self._jump(tgt)
                else:
                    self.pc += 1
                continue
            self._exec(mn, ops, t, va)
            self.pc += 1
        return {"pos": self.pos, "len": len(self.body),
                "closed": self.pos == len(self.body),
                "fields": self.fields, "gaps": self.gaps}

    def is_reader(self, va: int) -> bool:
        """只有真正含流读取(`call [rax+0x28]`)的函数才进入。"""
        code = self.disasm_at(va)
        if not code:
            return False
        return any(CALL_R28 in x["text"] for x in code)

    def _jump(self, tgt: int):
        idx = {x["va"]: i for i, x in enumerate(self.ins)}
        if tgt in idx:
            self.pc = idx[tgt]
            return True
        # 目标不在当前函数 → 跨函数跳转(尾调用/thunk)
        if self.depth > 12:
            self.gaps.append(f"depth limit at 0x{tgt:x}")
            return None
        if not self.is_reader(tgt):
            self.gaps.append(f"skip non-reader 0x{tgt:x}")
            return None
        if not self.enter(tgt):
            self.gaps.append(f"cannot enter 0x{tgt:x}")
            return None
        return True

    # --- 条件 ---
    def _cond(self, mn: str) -> bool:
        zf, sf, of = self.zf, self.sf, self.of
        if mn == "je":
            return zf
        if mn == "jne":
            return not zf
        if mn == "jl":
            return sf != of
        if mn == "jge":
            return sf == of
        if mn == "jle":
            return zf or (sf != of)
        if mn == "jg":
            return not zf and sf == of
        if mn == "jb":
            return self.cf
        if mn == "jae":
            return not self.cf
        if mn == "jbe":
            return self.cf or zf
        if mn == "ja":
            return not self.cf and not zf
        if mn == "js":
            return sf
        if mn == "jns":
            return not sf
        return False

    def _desc(self, expr: str) -> str:
        """把地址表达式翻成可读描述:对象内偏移 / 栈槽 / 流对象。"""
        p = parse_mem(expr)
        if p is None:
            return expr
        base, idx, scale, disp = p
        if base == "rsi" and idx is None:
            return f"[obj+0x{disp:x}]"
        if base == "rsp" and idx is None:
            return f"[stk+0x{disp:x}]"
        if base == "rbp" and idx is None:
            return f"[stk+0x{disp:x}]"
        return expr

    def _set_flags(self, a: int, b: int, width: int, sub: bool = True):
        bits = width * 8
        mask = (1 << bits) - 1
        sa = (a >> (bits - 1)) & 1
        sb = (b >> (bits - 1)) & 1
        if sub:
            r = (a - b) & mask
            self.cf = (a & mask) < (b & mask)
            of = sa != sb and ((r >> (bits - 1)) & 1) != sa
        else:
            r = (a + b) & mask
            self.cf = (a & mask) + (b & mask) > mask
            of = sa == sb and ((r >> (bits - 1)) & 1) != sa
        self.zf = r == 0
        self.sf = ((r >> (bits - 1)) & 1) == 1
        self.of = of

    def _val(self, s: str, width: int | None = None) -> int:
        s = s.strip()
        if s.startswith("[") or " ptr [" in s or "ptr gs:[" in s:
            v = self.load(s)
            return 0 if v is None else v
        if s in self.regs:
            return self.regs[s]
        if s in ALIAS:
            r, w = ALIAS[s]
            v = self.regs[r]
            return v & ((1 << (8 * w)) - 1) if w < 8 else v
        try:
            return int(s, 0)
        except ValueError:
            return 0

    def _exec(self, mn, ops, text, va):
        def w_of(expr: str) -> int:
            if "byte ptr" in expr:
                return 1
            if "word ptr" in expr:
                return 2
            if "dword ptr" in expr:
                return 4
            return 8

        if mn in ("movaps", "xorps", "movups"):
            return
        if mn == "movabs":
            self.regs[canon(ops[0])] = int(ops[1], 0)
            return
        if mn == "push":
            self.regs["rsp"] -= 8
            self.mem[self.regs["rsp"]] = self._val(ops[0])
            return
        if mn == "pop":
            v = self.mem.get(self.regs["rsp"], 0)
            self.regs["rsp"] += 8
            self.regs[canon(ops[0])] = v
            return
        if mn == "lea":
            a = self.addr(ops[1])
            self.regs[canon(ops[0])] = 0 if a is None else a
            if ops[0] == "rdx":
                self.last_dst = self._desc(ops[1])
            return
        if mn == "mov":
            d, s = ops[0], ops[1]
            if d == "r8d":
                try:
                    self.last_r8d = int(s, 0)
                except ValueError:
                    pass
            if d.startswith("[") or " ptr [" in d:
                self.store(d, self._val(s) & ((1 << (8 * w_of(d))) - 1))
            else:
                v = self._val(s)
                r = canon(d)
                if d in ALIAS:
                    _, w = ALIAS[d]
                    if w < 8:
                        v &= (1 << (8 * w)) - 1
                self.regs[r] = v
            return
        if mn == "movzx":
            src = ops[1]
            w = w_of(src)
            v = self._val(src)
            self.regs[canon(ops[0])] = v & ((1 << (8 * w)) - 1)
            return
        if mn in ("movzx", "movsx", "movsxd"):
            src = ops[1]
            w = w_of(src)
            v = self._val(src)
            if mn != "movzx" and v >> (8 * w - 1):
                v -= 1 << (8 * w)
            self.regs[canon(ops[0])] = v & ((1 << 64) - 1)
            return
        if mn == "cmp":
            w = max(w_of(ops[0]), w_of(ops[1]))
            self._set_flags(self._val(ops[0]) & ((1 << (8 * w)) - 1),
                            self._val(ops[1]) & ((1 << (8 * w)) - 1), w, True)
            return
        if mn == "test":
            w = w_of(ops[0])
            v = self._val(ops[0]) & self._val(ops[1])
            self.zf = v == 0
            self.sf = (v >> (8 * w - 1)) & 1 == 1
            self.cf = self.of = False
            return
        if mn in ("add", "sub", "and", "or", "xor", "imul", "shl", "shr", "ror"):
            d, s = ops[0], ops[1]
            a, b = self._val(d), self._val(s)
            w = w_of(d)
            if mn == "add":
                r = a + b
                self._set_flags(a, b, w, False)
            elif mn == "sub":
                r = a - b
                self._set_flags(a, b, w, True)
            elif mn == "and":
                r = a & b
                self.zf, self.sf, self.cf, self.of = r == 0, False, False, False
            elif mn == "or":
                r = a | b
                self.zf, self.sf, self.cf, self.of = r == 0, False, False, False
            elif mn == "xor":
                r = a ^ b
                self.zf, self.sf, self.cf, self.of = r == 0, False, False, False
            elif mn == "imul":
                r = a * b
            elif mn == "shl":
                r = a << b
            elif mn == "shr":
                r = (a & ((1 << 64) - 1)) >> b
            else:
                r = a
            if d.startswith("[") or " ptr [" in d:
                self.store(d, r & ((1 << (8 * w)) - 1))
            else:
                reg = canon(d)
                if d in ALIAS:
                    _, ww = ALIAS[d]
                    if ww < 8:
                        r &= (1 << (8 * ww)) - 1
                self.regs[reg] = r & ((1 << 64) - 1)
            return
        if mn in ("inc", "dec"):
            d = ops[0]
            a = self._val(d)
            w = w_of(d)
            r = a + 1 if mn == "inc" else a - 1
            if d.startswith("[") or " ptr [" in d:
                self.store(d, r & ((1 << (8 * w)) - 1))
            else:
                self.regs[canon(d)] = r & ((1 << 64) - 1)
            self.zf = (r & ((1 << (8 * w)) - 1)) == 0
            return
        if mn == "neg":
            self.regs[canon(ops[0])] = (-self._val(ops[0])) & ((1 << 64) - 1)
            return
        if mn == "sbb":
            self.regs[canon(ops[0])] = (self._val(ops[0]) - self._val(ops[1])) & ((1 << 64) - 1)
            return
        if mn == "call":
            tgt = ops[0]
            if "[rax + 0x28]" in tgt:
                self._do_stream_read(va)
                return
            if "[rax + 0x10]" in tgt:
                return
            self.calls.append(tgt)
            if "[" in tgt:
                return
            try:
                callee = int(tgt, 16)
            except ValueError:
                return
            if self.depth < 12 and self.is_reader(callee) and self.call_enter(callee):
                return
            self.regs["rax"] = 0
            self.zf = True
            return
        self.gaps.append(f"unhandled 0x{va:x} {text}")

    def _do_stream_read(self, va: int):
        w = self.last_r8d
        if w is None:
            self.gaps.append(f"no width at 0x{va:x}")
            return
        dstaddr = self.regs["rdx"]
        dstdesc = self.last_dst
        if dstdesc is None:
            dstdesc = f"0x{dstaddr:x}"
        if self.pos + w > len(self.body):
            self.gaps.append(f"overflow va=0x{va:x} w={w} pos={self.pos}")
            self.mem[self.stream + 0x10] = 1
            return
        raw = self.body[self.pos:self.pos + w]
        self.fields.append({"off": self.pos, "w": w, "dst": dstdesc,
                            "va": f"0x{va:x}", "raw": raw.hex()})
        val = int.from_bytes(raw, "little", signed=False)
        self.mem[dstaddr] = val
        self.mem[self.stream + 0x10] = 0
        self.pos += w


def run_body(body: bytes, version: int = 0xDC4) -> dict:
    P = _mod("p", "scripts/t89_probe.py")
    ins = P.parse("probe_t9_read")
    m = Machine(body, version, ins)
    r = m.run()
    r["gaps"] = m.gaps[:40]
    r["gap_n"] = len(m.gaps)
    r["calls"] = m.calls[:40]
    r["steps"] = m.steps
    return r


def load_rows(arch: str):
    W = _mod("w", "scripts/t85_fix1_wire.py")
    sz = W.member_size(arch, f"{arch}_db/table_9.dat")
    raw = W.C.payload(arch, f"{arch}_db/table_9.dat", sz)
    rows, _ = W.strict_chain(raw, 251)
    return raw, rows


def validate(version: int = 0xDC4) -> dict:
    out = {}
    for arch in ("client", "server"):
        raw, rows = load_rows(arch)
        ok = bad = 0
        first = None
        lens = set()
        for r in rows:
            b = raw[r["body_start"]:r["body_start"] + r["body_len"]]
            lens.add(r["body_len"])
            s = run_body(b, version)
            if s["closed"]:
                ok += 1
            else:
                bad += 1
                if first is None:
                    first = {"row": r["row"], "body_len": r["body_len"],
                             "consumed": s["pos"], "gaps": s["gaps"][:3]}
        out[arch] = {"rows": len(rows), "closed": ok, "open": bad,
                     "distinct_len": len(lens), "first_open": first}
    return {"version": hex(version), "result": out}


def selftest() -> int:
    P = _mod("p", "scripts/t89_probe.py")
    ins = P.parse("probe_t9_read")
    assert len(ins) > 2000
    assert canon("eax") == "rax" and canon("r12b") == "r12"
    assert parse_mem("[rsi + 0x488]") == ("rsi", None, 1, 0x488)
    assert parse_mem("[rsp + rcx*4 + 8]") == ("rsp", "rcx", 4, 8)
    assert _ops("qword ptr [rax + 0x28], 0x10") == ["qword ptr [rax + 0x28]", "0x10"]
    print("selftest OK", {"ins": len(ins)})
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="t9_read 符号执行器")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--validate", action="store_true")
    ap.add_argument("--trace", nargs=2, metavar=("ARCH", "ROW"))
    ap.add_argument("--version", default="0xdc4")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.validate:
        print(json.dumps(validate(int(a.version, 16)), indent=1, ensure_ascii=False))
        return 0
    if a.trace:
        arch, row = a.trace[0], int(a.trace[1])
        raw, rows = load_rows(arch)
        r = rows[row]
        b = raw[r["body_start"]:r["body_start"] + r["body_len"]]
        s = run_body(b, int(a.version, 16))
        print(f"row={row} body_len={len(b)} consumed={s['pos']} closed={s['closed']} "
              f"steps={s['steps']} gaps={s['gap_n']}")
        for f in s["fields"][:40]:
            print(f"  {f['off']:4d} w={f['w']} {f['dst']:<16s} {f['raw']}")
        if s["gaps"]:
            print("gaps:")
            for g in s["gaps"][:10]:
                print("  ", g)
        return 0
    ap.print_help()
    return 2


if __name__ == "__main__":
    sys.exit(main())
