#!/usr/bin/env python3
"""t89b_replay — replay t9_read (VA=0x14105d510) as a wire cursor machine.

Why: the static read list (t89b_readlin.py) sums to 213 B (r12b=1) / 63 B
(r12b=0), but the measured client row bodies span 46..449 B.  The difference is
not static: body length is *self-describing*.  Flag bytes and count words are
read from the wire and then gate further reads / set loop trip counts.  Only a
replay against real payload bytes can produce the per-row byte grid.

This tool executes the disassembly of t9_read (scratch/t89/probe_t9_read.txt)
against one row body.  `call qword ptr [rax+0x28]` is intercepted as
"consume r8d bytes at rdx from the payload cursor".

Success criterion (self-validating): the final cursor must equal the row body
length for every row.  If it does, the instruction model and the stub returns
are correct and the emitted read ledger IS the byte grid.

Usage:
  py -V:3.12 -I -B scripts/t89b_replay.py --side client --rows 251
  py -V:3.12 -I -B scripts/t89b_replay.py --side client --row 0 --trace
  py -V:3.12 -I -B scripts/t89b_replay.py --selftest
"""
from __future__ import annotations

import argparse
import json
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parents[1]
PROBE = ROOT / "scratch/t89/probe_t9_read.txt"
LINE = re.compile(r"fo=0x([0-9a-f]+) va=0x([0-9a-f]+) ([0-9a-f]+)\s+(.*)$")

# --- address space layout (synthetic; only relative structure matters) -------
PAYLOAD_BASE = 0x1000_0000
CONTAINER = 0x2000_0000
READER = 0x3000_0000     # reader object  ([obj] = vtable, [obj+0x10] = error)
VTABLE = 0x3000_1000
OBJSLOT = 0x3000_2000    # r13 points here; [r13] = READER
READ_FN = 0xDEAD_0001    # sentinel stored in vtable slot +0x28
PARAM4 = 0x4000_0000     # r9 -> r14 ; version word lives at +0x588
STACK = 0x7000_0000

# calls that return a pointer (bump-allocated scratch)
PTR_CALLS = {0x141750CC0}
# calls whose bool result is tested with `test al,al; je <epilogue>`
BOOL_CALLS = {
    0x1415CFEA0, 0x1410605B0, 0x140DB8980, 0x1411D1730,
    0x141571860, 0x141570A20, 0x1407E4940, 0x1408C9770,
    0x141073D90, 0x14141D570, 0x1407E53D0, 0x1410415F0,
    0x1415CFD70, 0x140B247F0, 0x1407E4890, 0x1407E4490,
    0x1410416A0, 0x14144C6A0, 0x140BA1B40, 0x14103AF20,
    0x14104F0B0, 0x141074100, 0x14155BE50, 0x14141D4A0,
    0x140FA1340, 0x141041A50,
}

REGS64 = ["rax", "rbx", "rcx", "rdx", "rsi", "rdi", "rbp", "rsp",
          "r8", "r9", "r10", "r11", "r12", "r13", "r14", "r15"]
R32 = {r + "d" if r[0] != "r" or len(r) == 2 else r + "d": r for r in REGS64}
ALIAS = {}
for _r in REGS64:
    ALIAS[_r] = (_r, 64)
# 32-bit aliases
_LEGACY = {"rax": ("eax", "ax", "al", "ah"),
           "rbx": ("ebx", "bx", "bl", "bh"),
           "rcx": ("ecx", "cx", "cl", "ch"),
           "rdx": ("edx", "dx", "dl", "dh"),
           "rsi": ("esi", "si", "sil", None),
           "rdi": ("edi", "di", "dil", None),
           "rbp": ("ebp", "bp", "bpl", None),
           "rsp": ("esp", "sp", "spl", None)}
for _r, (_e, _w, _l, _h) in _LEGACY.items():
    ALIAS[_e] = (_r, 32)
    ALIAS[_w] = (_r, 16)
    ALIAS[_l] = (_r, 8)
    if _h:
        ALIAS[_h] = (_r, 8)
for _i in range(8, 16):
    ALIAS[f"r{_i}d"] = (f"r{_i}", 32)
    ALIAS[f"r{_i}w"] = (f"r{_i}", 16)
    ALIAS[f"r{_i}b"] = (f"r{_i}", 8)
ALIAS["ah"] = ("rax", 8)  # unused, kept for safety


class Mem:
    """Sparse byte memory with a mapped payload window."""

    def __init__(self):
        self.d = {}
        self.payload = b""
        self.payload_base = PAYLOAD_BASE

    def map_payload(self, data: bytes):
        self.payload = data

    def rb(self, a: int) -> int:
        if self.payload_base <= a < self.payload_base + len(self.payload):
            return self.payload[a - self.payload_base]
        return self.d.get(a, 0)

    def wb(self, a: int, v: int):
        self.d[a & 0xFFFF_FFFF_FFFF] = v & 0xFF

    def rn(self, a: int, n: int) -> int:
        return int.from_bytes(bytes(self.rb(a + i) for i in range(n)), "little")

    def wn(self, a: int, n: int, v: int):
        v &= (1 << (8 * n)) - 1
        for i in range(n):
            self.wb(a + i, (v >> (8 * i)) & 0xFF)


class Fault(Exception):
    pass


class Machine:
    def __init__(self, ins, mem: Mem):
        self.ins = ins
        self.index = {x["va"]: i for i, x in enumerate(ins)}
        self.mem = mem
        self.r = {k: 0 for k in REGS64}
        self.zf = self.cf = self.sf = self.of = 0
        self.cursor = 0
        self.log = []
        self.bump = 0x5000_0000
        self.steps = 0

    # -- register helpers ---------------------------------------------------
    def get(self, name: str) -> int:
        reg, width = ALIAS[name]
        v = self.r[reg]
        if width == 64:
            return v
        mask = (1 << width) - 1
        return v & mask

    def set(self, name: str, val: int):
        reg, width = ALIAS[name]
        if width == 64:
            self.r[reg] = val & 0xFFFF_FFFF_FFFF_FFFF
        else:
            mask = (1 << width) - 1
            self.r[reg] = (self.r[reg] & ~mask) | (val & mask)

    # -- operand parsing ----------------------------------------------------
    def addr(self, s: str) -> int:
        """Evaluate a memory operand body (text between the brackets)."""
        s = s.strip()
        seg = None
        if ":" in s:
            seg, s = s.split(":", 1)
        if seg and seg != "gs" and seg != "fs":
            raise Fault("seg " + seg)
        if seg:
            return 0  # gs:[0x58] -> thread pointer; irrelevant here
        total = 0
        for term in re.split(r"\s*([+-])\s*", s):
            pass
        # split on +/- keeping signs
        parts = re.findall(r"([+-]?)\s*([^+-]+)", s)
        sign = 1
        for sgn, term in parts:
            term = term.strip()
            if sgn == "-":
                sign = -1
            elif sgn == "+":
                sign = 1
            m = re.fullmatch(r"([a-z0-9]+)\s*\*\s*(\d+)", term)
            if m:
                base = m.group(1)
                scale = int(m.group(2))
                if base in ALIAS:
                    total += sign * self.get(base) * scale
                else:
                    total += sign * int(base, 0) * scale
                sign = 1
                continue
            if term in ALIAS:
                total += sign * self.get(term)
            elif re.fullmatch(r"0x[0-9a-f]+|\d+", term):
                total += sign * int(term, 0)
            elif term == "rip":
                raise Fault("rip")
            else:
                raise Fault("term " + term)
            sign = 1
        return total & 0xFFFF_FFFF_FFFF

    def size_of(self, txt: str) -> int:
        if "byte ptr" in txt:
            return 1
        if "word ptr" in txt:
            return 2
        if "dword ptr" in txt:
            return 4
        if "qword ptr" in txt:
            return 8
        if "xmmword ptr" in txt:
            return 16
        raise Fault("size " + txt)

    def src_val(self, txt: str) -> int:
        txt = txt.strip()
        m = re.fullmatch(r"([a-z0-9]+)\s*ptr\s*\[(.*)\]", txt)
        if m:
            n = self.size_of(txt)
            return self.mem.rn(self.addr(m.group(2)), n)
        if txt in ALIAS:
            return self.get(txt)
        return int(txt, 0)

    def store(self, dst: str, val: int, n: int):
        m = re.fullmatch(r"([a-z0-9]+)\s*ptr\s*\[(.*)\]", dst.strip())
        if not m:
            self.set(dst.strip(), val)
            return
        self.mem.wn(self.addr(m.group(2)), n, val)

    # -- flags --------------------------------------------------------------
    def flags_sub(self, a: int, b: int, w: int):
        mask = (1 << w) - 1
        r = (a - b) & mask
        self.zf = 1 if r == 0 else 0
        self.cf = 1 if (a & mask) < (b & mask) else 0
        self.sf = 1 if (r >> (w - 1)) & 1 else 0
        sa = 1 if (a >> (w - 1)) & 1 else 0
        sb = 1 if (b >> (w - 1)) & 1 else 0
        sr = self.sf
        self.of = 1 if (sa != sb and sr != sa) else 0

    def flags_logic(self, r: int, w: int):
        self.zf = 1 if r == 0 else 0
        self.cf = self.of = 0
        self.sf = 1 if (r >> (w - 1)) & 1 else 0

    def jcc(self, op: str) -> bool:
        return {
            "je": self.zf == 1, "jz": self.zf == 1,
            "jne": self.zf == 0, "jnz": self.zf == 0,
            "jl": self.sf != self.of, "jnge": self.sf != self.of,
            "jle": self.zf == 1 or self.sf != self.of,
            "jg": self.zf == 0 and self.sf == self.of,
            "jge": self.sf == self.of,
            "jb": self.cf == 1, "jc": self.cf == 1,
            "jae": self.cf == 0, "jnc": self.cf == 0,
            "ja": self.cf == 0 and self.zf == 0,
            "jbe": self.cf == 1 or self.zf == 1,
        }[op]

    # -- wire read ----------------------------------------------------------
    def do_read(self, dest: int, width: int):
        self.log.append({"at": self.cursor, "w": width, "dest": dest})
        if self.cursor + width > len(self.mem.payload):
            self.mem.wn(READER + 0x10, 4, 1)  # error flag
            return
        for i in range(width):
            self.mem.wb(dest + i, self.mem.payload[self.cursor + i])
        self.cursor += width

    # -- main loop ----------------------------------------------------------
    def run(self, max_steps=2_000_000):
        i = 0
        while i < len(self.ins):
            self.steps += 1
            if self.steps > max_steps:
                raise Fault("step limit")
            x = self.ins[i]
            t = x["txt"]
            op = t.split()[0]
            nxt = i + 1
            if op == "mov" or op == "movabs":
                dst, src = [p.strip() for p in t[len(op):].split(",", 1)]
                if "ptr [" in dst:
                    self.store(dst, self.src_val(src), self.size_of(dst))
                else:
                    self.set(dst, self.src_val(src))
            elif op in ("movzx", "movsx", "movsxd"):
                dst, src = [p.strip() for p in t[len(op):].split(",", 1)]
                n = self.size_of(src) if "ptr" in src else (
                    ALIAS[src][1] // 8 if src in ALIAS else 4)
                v = self.src_val(src)
                if op == "movzx":
                    v &= (1 << (8 * n)) - 1
                else:
                    if v >> (8 * n - 1) & 1:
                        v -= 1 << (8 * n)
                    v &= 0xFFFF_FFFF_FFFF_FFFF
                self.set(dst, v)
            elif op == "lea":
                dst, src = [p.strip() for p in t[3:].split(",", 1)]
                m = re.fullmatch(r"\[(.*)\]", src)
                if not m:
                    raise Fault("lea " + src)
                self.set(dst, self.addr(m.group(1)))
            elif op in ("add", "sub", "and", "or", "xor", "cmp", "test"):
                a, b = [p.strip() for p in t[len(op):].split(",", 1)]
                va = self.src_val(a) if "ptr" not in a else self.src_val(a)
                vb = self.src_val(b)
                w = 64
                if a in ALIAS:
                    w = ALIAS[a][1]
                elif "ptr" in a:
                    w = 8 * self.size_of(a)
                mask = (1 << w) - 1
                va &= mask
                vb &= mask
                if op == "cmp":
                    self.flags_sub(va, vb, w)
                elif op == "test":
                    self.flags_logic(va & vb, w)
                else:
                    r = {"add": va + vb, "sub": va - vb, "and": va & vb,
                         "or": va | vb, "xor": va ^ vb}[op] & mask
                    if op in ("add", "sub"):
                        self.flags_sub(va, (-vb) & mask if op == "add" else vb, w)
                    else:
                        self.flags_logic(r, w)
                    self.store(a, r, w // 8)
            elif op in ("shl", "shr", "sar", "rol", "ror"):
                a, b = [p.strip() for p in t[len(op):].split(",", 1)]
                w = ALIAS[a][1] if a in ALIAS else 8 * self.size_of(a)
                mask = (1 << w) - 1
                v = self.src_val(a) & mask
                n = self.src_val(b) % w
                if op == "shl":
                    v = (v << n) & mask
                elif op == "shr":
                    v = v >> n
                elif op == "sar":
                    if v >> (w - 1) & 1:
                        v -= 1 << w
                    v = (v >> n) & mask
                elif op == "ror":
                    v = ((v >> n) | (v << (w - n))) & mask
                else:
                    v = ((v << n) | (v >> (w - n))) & mask
                self.store(a, v, w // 8)
            elif op in ("inc", "dec"):
                a = t[len(op):].strip()
                w = ALIAS[a][1] if a in ALIAS else 8 * self.size_of(a)
                mask = (1 << w) - 1
                v = (self.src_val(a) + (1 if op == "inc" else -1)) & mask
                self.flags_sub(v, 1 if op == "dec" else 0, w)
                self.store(a, v, w // 8)
            elif op == "imul":
                parts = [p.strip() for p in t[4:].split(",")]
                w = ALIAS[parts[0]][1] if parts[0] in ALIAS else 32
                v = self.src_val(parts[0]) * self.src_val(parts[-1])
                self.set(parts[0], v)
            elif op in ("push", "pop", "xorps", "movaps", "nop"):
                pass
            elif op == "sbb":
                a, b = [p.strip() for p in t[3:].split(",", 1)]
                w = ALIAS[a][1]
                mask = (1 << w) - 1
                v = (self.src_val(a) - self.src_val(b) - self.cf) & mask
                self.store(a, v, w // 8)
                self.flags_sub(self.src_val(a), self.src_val(b), w)
            elif op == "jmp":
                tgt = int(t[3:].strip(), 0)
                if tgt not in self.index:
                    break
                nxt = self.index[tgt]
            elif op in ("je", "jz", "jne", "jnz", "jl", "jle", "jg", "jge",
                        "jb", "jbe", "ja", "jae", "jc", "jnc", "jnge"):
                tgt = int(t.split()[-1], 0)
                if self.jcc(op):
                    if tgt not in self.index:
                        break
                    nxt = self.index[tgt]
            elif op == "call":
                arg = t[4:].strip()
                m = re.fullmatch(r"qword ptr \[(.*)\]", arg)
                if m:
                    tgt = self.mem.rn(self.addr(m.group(1)), 8)
                    if tgt == READ_FN:
                        dest = self.r["rdx"]
                        width = self.r["r8"] & 0xFFFFFFFF
                        self.do_read(dest, width)
                    else:
                        self.r["rax"] = 0
                else:
                    tgt = int(arg, 0)
                    if tgt in PTR_CALLS:
                        self.bump += 0x1000
                        self.r["rax"] = self.bump
                    elif tgt in BOOL_CALLS:
                        self.r["rax"] = 1
                    else:
                        self.r["rax"] = 0
            elif op == "ret":
                break
            else:
                raise Fault("op " + op)
            i = nxt
        return self.cursor


def load_ins(path=PROBE):
    ins = []
    for ln in path.read_text(encoding="utf-8", errors="replace").splitlines()[1:]:
        m = LINE.search(ln)
        if not m:
            continue
        ins.append({"va": int(m.group(2), 16), "txt": m.group(4).strip()})
    ins.sort(key=lambda x: x["va"])
    return ins


def setup(ins, body: bytes, r12b: int, version: int = 3569):
    mem = Mem()
    mem.map_payload(body)
    mem.wn(READER, 8, VTABLE)
    mem.wn(VTABLE + 0x28, 8, READ_FN)
    mem.wn(OBJSLOT, 8, READER)
    mem.wn(PARAM4 + 0x588, 2, version)
    mem.wn(STACK - 0xC8 + 0x140, 1, r12b)
    m = Machine(ins, mem)
    m.r["rcx"] = CONTAINER
    m.r["rdx"] = OBJSLOT
    m.r["r8"] = 0
    m.r["r9"] = PARAM4
    m.r["rsp"] = STACK
    return m


def run_row(ins, body: bytes, r12b: int):
    m = setup(ins, body, r12b)
    cur = m.run()
    return cur, m.log


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--side", default="client", choices=["client", "server"])
    ap.add_argument("--rows", type=int, default=0, help="limit rows (0=all)")
    ap.add_argument("--row", type=int, default=-1, help="single row index")
    ap.add_argument("--r12b", type=int, default=-1, help="force r12b (default: probe)")
    ap.add_argument("--trace", action="store_true")
    ap.add_argument("--out", default="scratch/t89/out/replay.json")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)

    sys.path.insert(0, str(ROOT / "scripts"))
    import t85_common as C

    if a.selftest:
        ins = load_ins()
        assert len(ins) > 2000, len(ins)
        body = bytes([0]) + bytes([0xFF] * 4) + bytes(range(20)) * 6
        cur, log = run_row(ins, body, 0)
        assert cur > 0, "no reads"
        assert all(e["w"] in (1, 2, 4, 8) for e in log), "bad width"
        print(f"selftest OK: ins={len(ins)} reads={len(log)} cursor={cur}")
        return 0

    if a.side == "client":
        payload = C.payload("client", "client_db/table_9.dat", 31956)
    else:
        payload = C.payload("server", "server_db/table_9.dat", 307564)
    dual = json.loads((ROOT / "scratch/t89/out/_dual.json").read_text(encoding="utf-8"))
    rows = dual[a.side]["rows_meta"]
    ins = load_ins()

    targets = [a.row] if a.row >= 0 else range(len(rows))
    if a.rows and a.row < 0:
        targets = list(targets)[:a.rows]

    results = []
    ok = 0
    for k in targets:
        r = rows[k]
        body = payload[r["start"]:r["start"] + r["len"]]
        best = None
        for r12 in ([a.r12b] if a.r12b >= 0 else [0, 1]):
            try:
                cur, log = run_row(ins, body, r12)
            except Fault as e:
                cur, log = -1, []
                if a.trace:
                    print("fault", e)
            if cur == r["len"]:
                best = (r12, cur, log)
                break
            if best is None:
                best = (r12, cur, log)
        r12, cur, log = best
        good = cur == r["len"]
        ok += good
        results.append({"ord": r["ord"], "len": r["len"], "r12b": r12,
                        "cursor": cur, "match": good,
                        "reads": [{"at": e["at"], "w": e["w"]} for e in log]})
        if a.trace:
            print(f"row {k} ord {r['ord']} len {r['len']} r12b={r12} cursor={cur} "
                  f"{'OK' if good else 'MISMATCH'} reads={len(log)}")
            if not good:
                for e in log[:40]:
                    print("   ", e)

    print(f"{a.side}: {ok}/{len(results)} rows reproduced exactly")
    if a.row < 0:
        out = ROOT / a.out
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"side": a.side, "ok": ok,
                                   "n": len(results), "rows": results},
                                  ensure_ascii=False), encoding="utf-8")
        print("wrote", out)
    return 0 if ok == len(results) else 1


if __name__ == "__main__":
    sys.exit(main())
