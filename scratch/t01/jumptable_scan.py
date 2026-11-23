"""Scan editor.exe .rdata for function-pointer jump tables (dispatch arrays).

A per-table parser dispatch would be an array of ~40-80 consecutive 8-byte RVAs
pointing into code. We look for runs of >=32 consecutive qwords that all decode
as plausible module addresses (0x140001000 .. image_end) — data arrays of
pointers. Reports runs with their element count and target spread.

Run: py -V:3.12 -I scratch/t01/jumptable_scan.py
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

EXE = Path(r"D:\tmp2b\fm24\input\editor.exe")
DELTA = 0xA00
RDATA_RAW_LO, RDATA_RAW_HI = 0x600, 0x1758600


def main() -> int:
    data = EXE.read_bytes()
    img_base = 0x140000000
    lo_ptr, hi_ptr = 0x140001000, img_base + 0x20000000
    runs = []
    i = RDATA_RAW_LO
    cur_start = None
    cur_len = 0
    step = 8
    while i + step <= RDATA_RAW_HI:
        v = struct.unpack_from("<Q", data, i)[0]
        ok = lo_ptr <= v < hi_ptr
        if ok:
            if cur_start is None:
                cur_start = i
            cur_len += 1
        else:
            if cur_len >= 32:
                runs.append((cur_start, cur_len))
            cur_start = None
            cur_len = 0
        i += step
    if cur_len >= 32:
        runs.append((cur_start, cur_len))

    print(f"pointer runs >=32 elements: {len(runs)}")
    for start, n in runs:
        vals = [struct.unpack_from("<Q", data, start + k * step)[0] for k in range(n)]
        spread = max(vals) - min(vals)
        # only report runs whose targets live in a 64MB window (code region-ish)
        if spread < 0x4000000:
            print(f"  off {start:#x} (RVA {start + DELTA:#x}) n={n} spread={spread:#x} first={vals[0]:#x} last={vals[-1]:#x}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
