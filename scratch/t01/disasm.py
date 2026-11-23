"""Capstone disassembler helper for t01 (stdlib + capstone).

Usage:
  py -V:3.12 -I scratch/t01/disasm.py <file_off_hex> <n_bytes>
Prints VA, bytes, and decoded instructions for editor.exe.
"""
from __future__ import annotations

import sys
from pathlib import Path

import capstone

EXE = Path(r"D:\tmp2b\fm24\input\editor.exe")
RDATA_DELTA = 0xA00  # VA = fileoff + 0xA00 in .rdata


def main() -> int:
    if len(sys.argv) != 3:
        print(__doc__)
        return 2
    off = int(sys.argv[1], 16)
    n = int(sys.argv[2], 16)
    data = EXE.read_bytes()[off:off + n]
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
    md.detail = False
    for ins in md.disasm(data, off + RDATA_DELTA):
        print(f"{ins.address:#x}  (off {ins.address - RDATA_DELTA:#x})  {ins.bytes.hex():<24} {ins.mnemonic} {ins.op_str}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
