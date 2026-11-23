#!/usr/bin/env python3
"""t88-fix5: dump a function's instruction stream + all 4CC immediates.

Usage: py -V:3.12 -I -B scripts/t88f5_dis.py --lo 0x1543ca0 --hi 0x1545200 [--grep 4cc]
"""
import argparse
import os
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXE = "D:/tmp2b/fm24/input/editor.exe"
BO = 0x140000a00


def cc(v):
    return struct.pack("<I", v)[::-1].decode("latin1")


def is4cc(v):
    return 0x20202020 <= v <= 0x7a7a7a7a and all(32 <= c < 127 for c in struct.pack("<I", v))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--lo", default="0x1543ca0")
    ap.add_argument("--hi", default="0x1545200")
    ap.add_argument("--only", default="", help="print only 4cc/cmp/jmp-table lines")
    a = ap.parse_args()
    b = open(EXE, "rb").read()
    if a.selftest:
        print("selftest ok, cc(0x736f6863)=%r" % cc(0x736f6863))
        return 0
    import capstone
    lo, hi = int(a.lo, 16), int(a.hi, 16)
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    n = 0
    for i in md.disasm(b[lo:hi], BO + lo):
        n += 1
        op = i.op_str
        line = "fo=%x va=%x %-8s %s" % (i.address - BO, i.address, i.mnemonic, op)
        if a.only:
            keep = False
            if i.mnemonic in ("cmp", "je", "jne", "ja", "jbe", "jmp", "lea", "mov") and ", 0x" in op:
                try:
                    v = int(op.split(", 0x")[-1], 16)
                    if is4cc(v):
                        keep = True
                        line += "   ; '%s'" % cc(v)
                except ValueError:
                    pass
            if not keep:
                continue
        print(line)
    print("# insns=%d" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
