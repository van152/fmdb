"""Row-reader probe v2 (parameterized, fast scan).

Searches a PE code region for mov/movzx [reg+disp8] instructions whose disp8 is
in a target set (known .dat row offsets), then reports 512B windows containing
the rare identity pair (0x72,0x76) -- candidate row parsers.

Usage:
  py -V:3.12 -I scripts/rowreader_probe2.py --exe <path> --lo <hex> --hi <hex> [--delta <hex>]
"""
from __future__ import annotations

import argparse
import struct
import sys
from collections import defaultdict
from pathlib import Path

import capstone


def main() -> int:
    ap = argparse.ArgumentParser(description="Probe for .dat row-parser code windows.")
    ap.add_argument("--exe", required=True)
    ap.add_argument("--lo", required=True)
    ap.add_argument("--hi", required=True)
    ap.add_argument("--delta", default="A00")
    ap.add_argument("--window", type=int, default=512)
    args = ap.parse_args()

    DELTA = int(args.delta, 16)
    LO, HI = int(args.lo, 16), int(args.hi, 16)
    TARGETS = {0x34, 0x38, 0x40, 0x72, 0x76}
    data = Path(args.exe).read_bytes()
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

    hits = defaultdict(list)
    pos = LO
    while True:
        i = data.find(b"\x8b", pos, HI - 3)
        if i < 0:
            break
        pos = i + 1
        modrm = data[i + 1]
        if (modrm >> 6) == 1 and (modrm & 7) != 4:  # disp8, not sib
            disp = data[i + 2]
            if disp in TARGETS:
                hits[disp].append(i)
    for pat in (b"\x0f\xb6", b"\x0f\xb7"):
        pos = LO
        while True:
            i = data.find(pat, pos, HI - 4)
            if i < 0:
                break
            pos = i + 1
            modrm = data[i + 2]
            if (modrm >> 6) == 1 and (modrm & 7) != 4:
                disp = data[i + 3]
                if disp in TARGETS:
                    hits[disp].append(i)

    all_pos = sorted(p for lst in hits.values() for p in lst)
    print(f"hits: {len(all_pos)}  per-offset: {({hex(k): len(v) for k, v in sorted(hits.items())})}")

    merged = []
    n = len(all_pos)
    for i in range(n):
        j = i
        while j < n and all_pos[j] - all_pos[i] < args.window:
            j += 1
        win = all_pos[i:j]
        distinct = {data[p + 2] if data[p] == 0x8B else data[p + 3] for p in win}
        if 0x72 in distinct and 0x76 in distinct:
            s, e = win[0], win[-1]
            if merged and s <= merged[-1][1]:
                merged[-1][1] = max(e, merged[-1][1])
            else:
                merged.append([s, e])

    print(f"pair-windows (0x72+0x76): {len(merged)}")
    for s, e in merged[:10]:
        print(f"\n== off {s:#x}..{e:#x} (RVA {s + DELTA:#x})")
        for ins in list(md.disasm(data[s:e + 16], s + DELTA))[:20]:
            print(f"   {ins.address:#x}: {ins.mnemonic} {ins.op_str}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
