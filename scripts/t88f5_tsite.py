#!/usr/bin/env python3
"""t88-fix5: disassemble around the table_45 (type 0x2d) registration site.

Usage: py -V:3.12 -I -B scripts/t88f5_tsite.py [--selftest] [--lo 0xf06b80] [--hi 0xf06dc0]
"""
import argparse
import sys as _cfg_sys
from pathlib import Path as _cfg_pathlib
_cfg_sys.path.insert(0, str(_cfg_pathlib(__file__).resolve().parent))
import fm24_config as _cfg
import os
import sys

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

EXE = str(_cfg.EDITOR_EXE)
BO = 0x140000a00


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--lo", default="0xf06b80")
    ap.add_argument("--hi", default="0xf06dc0")
    a = ap.parse_args()
    if a.selftest:
        b = open(EXE, "rb").read()
        print("selftest bytes@0xf06c70:", b[0xf06c70:0xf06c84].hex())
        return 0 if b[0xf06c70:0xf06c72] == b"\xba\x2d" else 1
    import capstone
    b = open(EXE, "rb").read()
    lo, hi = int(a.lo, 16), int(a.hi, 16)
    va = BO + lo
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    for i in md.disasm(b[lo:hi], va):
        print("fo=%x va=%x  %-8s %s" % (i.address - BO, i.address, i.mnemonic, i.op_str))
    return 0


if __name__ == "__main__":
    sys.exit(main())
