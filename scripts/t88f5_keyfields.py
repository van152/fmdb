#!/usr/bin/env python3
"""t88-fix5: find functions that touch both [rec+0x4c] and [rec+0x5e] (STARTING_RECORD reader/writer).

Usage: py -V:3.12 -I -B scripts/t88f5_keyfields.py [--selftest] [--win 0x400]
"""
import argparse
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg
import os
import re
import struct
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXE = str(_cfg.EDITOR_EXE)
BO = 0x140000a00

# opcodes whose modrm may carry mod=01 disp8
PREFIXES = [b"\x0f\xb6", b"\x0f\xbe", b"\x0f\xb7", b"\x0f\xbf",
            b"\x88", b"\x8a", b"\x89", b"\x8b", b"\x66\x89", b"\x66\x8b",
            b"\xc7", b"\xc6", b"\x83", b"\x81", b"\x39", b"\x3b", b"\x85"]


def hits(b, disp):
    out = []
    for pre in PREFIXES:
        pat = re.compile(re.escape(pre) + b"[\x40-\x7f]" + re.escape(bytes([disp])), re.S)
        for m in pat.finditer(b):
            out.append(m.start())
    return sorted(set(out))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--win", default="0x400")
    a = ap.parse_args()
    b = open(EXE, "rb").read()
    if a.selftest:
        print("selftest bytes=%d" % len(b))
        return 0
    win = int(a.win, 16)
    h4c = hits(b, 0x4C)
    h5e = hits(b, 0x5E)
    print("disp0x4c hits=%d disp0x5e hits=%d" % (len(h4c), len(h5e)))
    import bisect
    pairs = []
    for fo in h5e:
        i = bisect.bisect_left(h4c, fo - win)
        while i < len(h4c) and h4c[i] <= fo + win:
            pairs.append((h4c[i], fo, abs(h4c[i] - fo)))
            i += 1
    pairs.sort(key=lambda p: p[2])
    print("co-located pairs=%d" % len(pairs))
    for a4, a5, d in pairs[:25]:
        print("  fo4c=0x%x fo5e=0x%x gap=0x%x  va5e=0x%x" % (a4, a5, d, BO + a5))
    return 0


if __name__ == "__main__":
    sys.exit(main())
