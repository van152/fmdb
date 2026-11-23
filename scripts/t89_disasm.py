#!/usr/bin/env python3
"""t89_disasm — 用 capstone 反汇编 editor.exe 指定 VA 区间(只读)。

用法:
  py -V:3.12 -I -B scripts/t89_disasm.py --va 0x1408386a0 --len 0x180
  py -V:3.12 -I -B scripts/t89_disasm.py --selftest
"""
from __future__ import annotations

import argparse
import pathlib
import sys

EXE = pathlib.Path("D:/tmp2b/fm24/input/editor.exe")
SECTIONS = [
    (".rdata", 0x1000, 0x1758000, 0x600),
    (".debug", 0x1759000, 0x325000, 0x1758600),
    (".sbss", 0x1A7E000, 0xE9000, 0x1A7D000),
    (".code", 0x1B67000, 0x93000, 0x1ABC600),
    (".data", 0x47EB000, 0x4142C, 0x467F200),
]
IMAGE_BASE = 0x140000000


def va_to_fo(va: int):
    rva = va - IMAGE_BASE
    for name, sva, size, sfo in SECTIONS:
        if sva <= rva < sva + size:
            return sfo + (rva - sva)
    return None


def disasm(va: int, n: int) -> list[dict]:
    import capstone
    db = EXE.read_bytes()
    fo = va_to_fo(va)
    if fo is None:
        raise SystemExit(f"VA 0x{va:x} 不在已收录节内")
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = True
    out = []
    for ins in md.disasm(db[fo:fo + n], va):
        out.append({"va": ins.address, "bytes": ins.bytes.hex(),
                    "mn": ins.mnemonic, "op": ins.op_str,
                    "text": f"{ins.mnemonic} {ins.op_str}".strip()})
    return out


def selftest() -> int:
    r = disasm(0x1408386a0, 0x40)
    assert r[0]["mn"] == "push" and r[0]["op"] == "rbp", r[0]
    r2 = disasm(0x14105d510, 0x10)
    assert r2[0]["mn"] == "push" and r2[0]["op"] == "r15", r2[0]
    print("selftest OK", {"item_reader_ins": len(disasm(0x1408386a0, 0x180))})
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description="editor.exe capstone 反汇编")
    ap.add_argument("--va", help="起始 VA")
    ap.add_argument("--len", default="0x100", help="字节数")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.va:
        ap.print_help()
        return 2
    for x in disasm(int(a.va, 16), int(a.len, 0)):
        print(f"0x{x['va']:x} {x['bytes']:<20s} {x['text']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
