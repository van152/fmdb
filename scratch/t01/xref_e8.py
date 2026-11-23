"""Find all e8 rel32 call sites targeting given file offsets in editor.exe.

Usage: py -V:3.12 -I scratch/t01/xref_e8.py 83abf0 [83caf0 ...]
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

EXE = Path(r"D:\tmp2b\fm24\input\editor.exe")


def main() -> int:
    targets = {int(a, 16) for a in sys.argv[1:]}
    data = EXE.read_bytes()
    hits: dict[int, list[int]] = {t: [] for t in targets}
    pos = 0
    needle = b"\xe8"
    while True:
        i = data.find(needle, pos)
        if i < 0:
            break
        pos = i + 1
        if i + 5 > len(data):
            continue
        rel = struct.unpack_from("<i", data, i + 1)[0]
        tgt = i + 5 + rel
        if tgt in hits and 0 <= tgt < len(data):
            hits[tgt].append(i)
    for t, sites in hits.items():
        print(f"target off {t:#x} (VA {t + 0xA00:#x}): {len(sites)} direct e8 call sites")
        for s in sites[:80]:
            print(f"   call at off {s:#x} (VA {s + 0xA00:#x})")
        if len(sites) > 80:
            print(f"   ... +{len(sites) - 80} more")
    return 0


if __name__ == "__main__":
    sys.exit(main())
