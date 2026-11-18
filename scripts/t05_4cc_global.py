"""t05_4cc_global — 全局 4CC 表: 不依赖 reader 邻近性。

背景(E42 之后的发现):
    city 的 4CC 分发链在 0xe55000 一带, 而它的 reader body 在 0x3aa5550,
    相距 0x2C 万字节 —— 说明"dispatch 链紧邻 reader"的假设只对手写优化的
    injury/type22 成立。必须建立**全局** 4CC 表。

做法(纯字节搜索, 不做 capstone 全扫, 快 100 倍):
    cmp reg, imm32 的机器码是 81 /7 id, 常见:
        81 FA <imm32>  cmp edx, imm32
        81 FB <imm32>  cmp ebx, imm32
        81 F9 <imm32>  cmp ecx, imm32
        3D    <imm32>  cmp eax, imm32
    imm32 若 4 字节全为可打印 ASCII 的**反序**, 即为 4CC。
    命中后从该处反汇编 96B, 找行缓冲成员访问 [reg+OFF] 得到字段偏移。

输出: {4CC: [{file_off, off, size, kind, va}]}  -> scratch/t05/4cc_global.json

用法:
    py -V:3.12 -I -B scripts/t05_4cc_global.py
    py -V:3.12 -I -B scripts/t05_4cc_global.py --code Clat   # 查单个
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "scratch/t05/4cc_global.json"

# 带 imm32 的 cmp 编码
CMP_PREFIXES = (
    b"\x81\xfa", b"\x81\xfb", b"\x81\xf9", b"\x81\xf8",
    b"\x81\xfe", b"\x81\xff", b"\x81\xfd", b"\x81\xfc",
    b"\x3d",
)
LOOKAHEAD = 96

ACCESS_SIZE = {"byte": 1, "word": 2, "dword": 4, "qword": 8}
RE_MEM = re.compile(r"^(?:mov|movzx|movsx|movsxd|movss|movsd)\s+([a-z0-9]+),\s*(byte|word|dword|qword)?\s*ptr\s*\[([a-z0-9]+)\s*\+\s*(0x[0-9a-f]+)\]$")
RE_MEM_ST = re.compile(r"^mov\s+(byte|word|dword|qword)?\s*ptr\s*\[([a-z0-9]+)\s*\+\s*(0x[0-9a-f]+)\],\s*([a-z0-9]+)$")
BUF_REGS = {"rsi", "rdi", "rcx", "rbx", "rdx", "r8", "r9", "r12", "r13", "r14", "r15"}
OFF_MIN, OFF_MAX = 0x20, 0x400


def mem_access(ins):
    text = ins.mnemonic + " " + ins.op_str
    m = RE_MEM.match(text)
    if m and m.group(3) in BUF_REGS:
        off = int(m.group(4), 16)
        if OFF_MIN <= off <= OFF_MAX:
            return off, ACCESS_SIZE.get(m.group(2) or "dword", 4), "read"
    m = RE_MEM_ST.match(text)
    if m and m.group(2) in BUF_REGS:
        off = int(m.group(3), 16)
        if OFF_MIN <= off <= OFF_MAX:
            return off, ACCESS_SIZE.get(m.group(1) or "dword", 4), "write"
    return None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--code", default=None, help="只查某个 4CC")
    ap.add_argument("--out", default=str(OUT))
    ap.add_argument("--lookahead", type=int, default=LOOKAHEAD)
    args = ap.parse_args()

    from capstone import CS_ARCH_X86, CS_MODE_64, Cs
    import importlib.util
    spec = importlib.util.spec_from_file_location("_pe", ROOT / "scripts/t05_pe.py")
    pm = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pm)
    pe = pm.default()
    raw = pe.raw
    md = Cs(CS_ARCH_X86, CS_MODE_64)

    # 只在可执行段里搜(代码在 .rdata/.reloc)
    ranges = []
    for s in pe._secs:
        if s["exec"] and s["rawsize"] > 0:
            ranges.append((s["raw"], s["raw"] + min(s["rawsize"], len(raw))))
    print(f"可执行段 {len(ranges)} 个, 合计 {sum(b-a for a,b in ranges)/1e6:.1f} MB")

    hits: list[tuple[int, str]] = []      # (file_off_of_imm, code)
    for plen_prefix in CMP_PREFIXES:
        L = len(plen_prefix)
        for a, b in ranges:
            i = a
            while True:
                i = raw.find(plen_prefix, i, b)
                if i < 0:
                    break
                imm_at = i + L
                if imm_at + 4 <= b:
                    imm = raw[imm_at:imm_at + 4]
                    if all(32 <= c < 127 for c in imm):
                        code = imm[::-1].decode("latin1")
                        if code.isalnum() or (code[:1].isalpha() and all(32 <= c < 127 for c in imm)):
                            hits.append((i, code))
                i += 1
    print(f"4CC cmp 候选 {len(hits)} 处, 去重 code {len({c for _, c in hits})} 个")

    table: dict[str, list[dict]] = {}
    seen_code_off: set[tuple[str, int]] = set()
    for off, code in hits:
        if args.code and code != args.code:
            continue
        base_va = pe.f2va(off)
        if base_va is None:
            continue
        ins = list(md.disasm(raw[off:off + 12], base_va))
        if not ins or ins[0].mnemonic != "cmp":
            continue
        # 1) 跟随 je/jne 目标(真正的 getter/setter 体)
        acc = None
        block = list(md.disasm(raw[off:off + args.lookahead], base_va))
        for x in block[1:4]:
            if x.mnemonic not in ("je", "jz", "jne", "jnz"):
                continue
            try:
                tgt_va = int(x.op_str.replace(" ", ""), 0)
            except ValueError:
                continue
            tgt = pe.va2f(tgt_va)
            if tgt is None:
                continue
            for y in md.disasm(raw[tgt:tgt + 64], tgt_va):
                a = mem_access(y)
                if a:
                    acc = (a[0], a[1], a[2], hex(y.address))
                    break
                if y.mnemonic == "ret":
                    break
            break
        # 2) fall-through(setter 内联形态)
        if acc is None:
            for x in block[1:]:
                a = mem_access(x)
                if a:
                    acc = (a[0], a[1], a[2], hex(x.address))
                    break
                if x.mnemonic == "ret":
                    break
        if not acc:
            continue
        key = (code, acc[0])
        if key in seen_code_off:
            continue
        seen_code_off.add(key)
        rec = {"file_off": hex(off), "object_off": acc[0], "size": acc[1],
               "kind": acc[2], "access_va": acc[3], "section": pe.section_of(off)}
        table.setdefault(code, []).append(rec)

    Path(args.out).write_text(json.dumps({
        "note": "全局 4CC 表: 通过 cmp reg,imm32 的机器码定位(imm32 为 4CC 反序),"
                "再从后续 96B 内取行缓冲成员访问 [reg+OFF]。off 为对象内偏移, 与 reader 的 lea rdx,[obj+OFF] 可对齐。",
        "exe_sha256": __import__("hashlib").sha256(raw).hexdigest(),
        "codes": len(table),
        "table": table,
    }, ensure_ascii=False, indent=1), encoding="utf-8")

    print(f"带成员访问的 4CC: {len(table)} 个 -> {args.out}")
    if args.code:
        print()
        for r in table.get(args.code, []):
            print(f"  {args.code}: off={hex(r['object_off'])} size={r['size']} kind={r['kind']} "
                  f"@{r['file_off']} ({r['section']})")
    else:
        multis = sum(1 for v in table.values() if len({r["object_off"] for r in v}) == 1)
        print(f"其中偏移唯一的(可直接当字段偏移): {multis}")
        for code in sorted(table)[:25]:
            offs = sorted({r["object_off"] for r in table[code]})
            print(f"  {code:<5} -> {[hex(o) for o in offs[:4]]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
