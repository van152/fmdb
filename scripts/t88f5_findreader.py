#!/usr/bin/env python3
"""t88-fix5: locate STARTING_RECORD reader/writer via mem-offset write sites.

Usage: py -V:3.12 -I -B scripts/t88f5_findreader.py [--selftest] [--off 0x5e]
"""
import argparse
import collections
import os
import re
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXE = "D:/tmp2b/fm24/input/editor.exe"
BO = 0x140000a00
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT3 = os.path.join(ROOT, "scratch", "t88", "out3")


def load_ins(lo, hi):
    import capstone
    b = open(EXE, "rb").read()
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    return b, list(md.disasm(b[lo - BO:hi - BO], lo))


def func_start(ins, idx, back=4000):
    """walk back to nearest 'push rbp/... int3' boundary."""
    k = idx
    while k > 0 and idx - k < back:
        i = ins[k - 1]
        if i.mnemonic == "int3" or (i.mnemonic == "ret" and i.op_str in ("", "0x0")):
            return k
        k -= 1
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--lo", default="0x141540000")
    ap.add_argument("--hi", default="0x141548000")
    a = ap.parse_args()
    if a.selftest:
        b, ins = load_ins(0x141544b00, 0x141545e00)
        print("selftest insns=%d first=%s" % (len(ins), ins[0].mnemonic))
        return 0 if len(ins) > 100 else 1
    b, ins = load_ins(int(a.lo, 16), int(a.hi, 16))
    hits = collections.defaultdict(list)
    for k, i in enumerate(ins):
        m = re.search(r"\[(\w+) \+ (0x[0-9a-f]+)\]", i.op_str)
        if not m:
            continue
        off = int(m.group(2), 16)
        if 0x40 <= off <= 0x60:
            hits[off].append((k, i.address, i.mnemonic, i.op_str))
    for off in sorted(hits):
        rows = hits[off]
        print("+0x%02x  n=%d  %s" % (off, len(rows),
                                     " ".join("%x:%s %s" % (r[1], r[2], r[3]) for r in rows[:4])))
    return 0


if __name__ == "__main__":
    sys.exit(main())
