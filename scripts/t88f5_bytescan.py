#!/usr/bin/env python3
"""t88-fix5: raw-byte scan for STARTING_RECORD mem writes (disp8=0x5d etc).

Usage: py -V:3.12 -I -B scripts/t88f5_bytescan.py [--selftest] [--disp 5d]
"""
import argparse
import os
import re
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXE = "D:/tmp2b/fm24/input/editor.exe"
BO = 0x140000a00
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
OUT3 = os.path.join(ROOT, "scratch", "t88", "out3")

# mov/movzx/movsx/cmp with mod=01 (disp8) and given displacement
FORMS = [
    (b"\x0f\xb6", "movzx8"), (b"\x0f\xbe", "movsx8"),
    (b"\x0f\xb7", "movzx16"), (b"\x0f\xbf", "movsx16"),
    (b"\x88", "mov8_s"), (b"\x8a", "mov8_l"),
    (b"\x89", "mov32_s"), (b"\x8b", "mov32_l"),
    (b"\x66\x89", "mov16_s"), (b"\x66\x8b", "mov16_l"),
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--disp", default="5d")
    a = ap.parse_args()
    b = open(EXE, "rb").read()
    if a.selftest:
        print("selftest exe_bytes=%d" % len(b))
        return 0 if len(b) > 10_000_000 else 1
    d = int(a.disp, 16)
    hits = []
    for pre, name in FORMS:
        # modrm mod=01 -> 0x40..0x7f ; displacement follows modrm
        pat = re.compile(re.escape(pre) + b"[\x40-\x7f]" + re.escape(bytes([d])), re.S)
        for m in pat.finditer(b):
            fo = m.start()
            hits.append((fo, 0x140000a00 + fo, name, m.group(0).hex()))
    hits.sort()
    print("disp=0x%02x hits=%d" % (d, len(hits)))
    for fo, va, name, by in hits[:40]:
        print("  fo=0x%x va=0x%x %-9s %s" % (fo, va, name, by))
    return 0


if __name__ == "__main__":
    sys.exit(main())
