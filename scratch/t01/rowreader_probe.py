"""Probe for comp .dat row-reader: windows with >=3 of the known row-offset disp8s.

Known client comp row anchors (from db_tables_big, L2): offsets 0x34(ccti) 0x38(cnti)
0x40(cpcm) 0x72(rdui) 0x76(duni). A row parser touches several of these within a
small code window. We scan .rdata for mov reg,[reg+disp8] / movzx forms whose
disp8 hits these values, then report windows (512B) containing >=3 distinct hits.

Run: py -V:3.12 -I scratch/t01/rowreader_probe.py
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import capstone

EXE = Path(r"D:\tmp2b\fm24\input\editor.exe")
DELTA = 0xA00
LO, HI = 0x600, 0x1758600
TARGETS = {0x34, 0x38, 0x40, 0x72, 0x76}
WINDOW = 512
MIN_DISTINCT = 3


def main() -> int:
    data = EXE.read_bytes()
    md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

    hits = defaultdict(list)  # offset_value -> [code_positions]
    pos = LO
    while pos < HI - 4:
        b = data[pos]
        if b == 0x8B:  # mov r32, r/m
            modrm = data[pos + 1]
            if (modrm >> 6) == 1:  # mod=01 -> disp8
                disp = data[pos + 2]
                if disp in TARGETS:
                    hits[disp].append(pos)
            pos += 1
        elif b == 0x0F and data[pos + 1] in (0xB6, 0xB7):  # movzx r32, byte/word
            modrm = data[pos + 2]
            if (modrm >> 6) == 1:
                disp = data[pos + 3]
                if disp in TARGETS:
                    hits[disp].append(pos)
            pos += 2
        else:
            pos += 1

    all_pos = sorted(p for lst in hits.values() for p in lst)
    print(f"total disp8 hits: {len(all_pos)}  per-offset: {({hex(k): len(v) for k, v in sorted(hits.items())})}")

    # sliding window over positions; require BOTH 0x72 and 0x76 (rare identity pair)
    results = []
    n = len(all_pos)
    for i in range(n):
        j = i
        while j < n and all_pos[j] - all_pos[i] < WINDOW:
            j += 1
        win = all_pos[i:j]
        distinct = {data[p + 2] if data[p] == 0x8B else data[p + 3] for p in win}
        if 0x72 in distinct and 0x76 in distinct:
            results.append((win[0], win[-1], sorted(distinct)))
    # dedupe overlapping windows
    merged = []
    for s, e, d in results:
        if merged and s <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(e, merged[-1][1]), sorted(set(merged[-1][2]) | set(d)))
        else:
            merged.append((s, e, d))

    print(f"windows with >={MIN_DISTINCT} distinct target offsets: {len(merged)}")
    for s, e, d in merged[:20]:
        print(f"\n== code window off {s:#x}..{e:#x} (RVA {s+DELTA:#x}) offsets={d}")
        insns = list(md.disasm(data[s:e + 16], s + DELTA))
        for ins in insns[:24]:
            print(f"   {ins.address:#x}: {ins.mnemonic} {ins.op_str}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
