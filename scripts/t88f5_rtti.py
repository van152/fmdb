#!/usr/bin/env python3
"""t88-fix5: locate STARTING_RECORD vtable via RTTI name string.

Usage: py -V:3.12 -I -B scripts/t88f5_rtti.py [--selftest] [--name STARTING_RECORD]
"""
import argparse
import os
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXE = "D:/tmp2b/fm24/input/editor.exe"
BO = 0x140000a00


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--name", default="STARTING_RECORD")
    a = ap.parse_args()
    b = open(EXE, "rb").read()
    if a.selftest:
        print("selftest exe=%d" % len(b))
        return 0
    needle = a.name.encode()
    offs = []
    i = b.find(needle)
    while i >= 0:
        offs.append(i)
        i = b.find(needle, i + 1)
    print("name occurrences=%d" % len(offs))
    for fo in offs[:12]:
        lo = b.rfind(b"\x00", max(0, fo - 160), fo)
        s = b[lo + 1:fo + len(needle) + 4]
        try:
            txt = s.decode("latin1")
        except Exception:
            txt = "?"
        print("  fo=0x%x va=0x%x ctx=%r" % (fo, BO + fo, txt[-120:]))
    # Type descriptor: 16 bytes before name string is vtable ptr(8) + spare(8)
    for fo in offs:
        for back in (16,):
            tdo = fo - back
            vt = struct.unpack_from("<Q", b, tdo)[0]
            print("  TD fo=0x%x vtable=0x%x (fo 0x%x)" % (tdo, vt, vt - BO))
    return 0


if __name__ == "__main__":
    sys.exit(main())
