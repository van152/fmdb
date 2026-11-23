#!/usr/bin/env python3
"""t88-fix5: find serializer-like functions (many distinct disp 0x20..0x5f on one base).

Usage: py -V:3.12 -I -B scripts/t88f5_serial.py [--selftest] [--lo 0x1530000] [--hi 0x1560000]
"""
import argparse
import collections
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXE = "D:/tmp2b/fm24/input/editor.exe"
BO = 0x140000a00


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--lo", default="0x1530000")
    ap.add_argument("--hi", default="0x1560000")
    ap.add_argument("--min", type=int, default=8)
    a = ap.parse_args()
    b = open(EXE, "rb").read()
    if a.selftest:
        print("selftest exe=%d" % len(b))
        return 0
    import capstone
    lo, hi = int(a.lo, 16), int(a.hi, 16)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    cur = None
    acc = collections.defaultdict(set)
    funcs = {}
    for i in md.disasm(b[lo:hi], BO + lo):
        if cur is None:
            cur = i.address
            acc = collections.defaultdict(set)
        m = re.search(r"\[(\w+) \+ (0x[0-9a-f]+)\]", i.op_str)
        if m:
            off = int(m.group(2), 16)
            if 0x18 <= off <= 0x5f:
                acc[m.group(1)].add(off)
        if i.mnemonic in ("ret", "int3"):
            best = max(acc.items(), key=lambda kv: len(kv[1])) if acc else None
            if best and len(best[1]) >= a.min:
                funcs[cur] = (best[0], sorted(best[1]))
            cur = None
    print("serializer candidates=%d" % len(funcs))
    for addr, (reg, offs) in sorted(funcs.items()):
        print("fo=%x va=%x base=%s n=%d offs=%s" % (
            addr - BO, addr, reg, len(offs), " ".join("0x%x" % o for o in offs)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
