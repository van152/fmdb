"""PE facts for editor.exe / fm.exe: image base, section table, file-offset -> VA.

Commander-owned tool for t01. stdlib only. Run: py -V:3.12 -I scratch/t01/probe_pe.py
"""
from __future__ import annotations

import struct
import sys
from pathlib import Path

EXE = Path(r"D:\tmp2b\fm24\input\editor.exe")


def pe_facts(data: bytes) -> dict:
    e_lfanew = struct.unpack_from("<I", data, 0x3C)[0]
    assert data[e_lfanew:e_lfanew + 4] == b"PE\0\0", "not a PE"
    coff = e_lfanew + 4
    machine, nsec, _, _, _, opt_size = struct.unpack_from("<HHIIIH", data, coff)
    opt = coff + 20
    magic = struct.unpack_from("<H", data, opt)[0]
    img_base = struct.unpack_from("<Q" if magic == 0x20B else "<I", data, opt + 24)[0]
    secs = []
    st = opt + opt_size
    for i in range(nsec):
        off = st + i * 40
        name = data[off:off + 8].rstrip(b"\0").decode(errors="replace")
        vsize, vaddr, rsize, rptr = struct.unpack_from("<IIII", data, off + 8)
        secs.append({"name": name, "vsize": vsize, "vaddr": vaddr, "rsize": rsize, "rptr": rptr})
    return {"machine": hex(machine), "image_base": img_base, "sections": secs}


def off_to_va(sections: list, img_base: int, off: int) -> str:
    for s in sections:
        if s["rptr"] <= off < s["rptr"] + s["rsize"]:
            return hex(img_base + s["vaddr"] + (off - s["rptr"]))
    return "unmapped"


def e8_targets(data: bytes, lo: int, hi: int) -> list:
    out = []
    for i in range(lo, hi):
        if data[i] == 0xE8:
            rel = struct.unpack_from("<i", data, i + 1)[0]
            tgt = i + 5 + rel
            out.append({"call_at_off": hex(i), "target_off": hex(tgt)})
    return out


def main() -> int:
    data = EXE.read_bytes()
    facts = pe_facts(data)
    print(f"exe: {EXE}  size={len(data):,}")
    print(f"image_base={facts['image_base']:#x}  machine={facts['machine']}")
    for s in facts["sections"]:
        print(f"  {s['name']:<8} vaddr={s['vaddr']:#x} vsize={s['vsize']:#x} rptr={s['rptr']:#x} rsize={s['rsize']:#x}")
    for probe in (0xEBF060, 0xEBF093, 0xEBF153, 0xEC2009, 0xEC152C):
        print(f"  off {probe:#x} -> VA {off_to_va(facts['sections'], facts['image_base'], probe)}")
    print("e8 call targets in 0xebf000..0xebf200:")
    for t in e8_targets(data, 0xEBF000, 0xEBF200):
        va = off_to_va(facts["sections"], facts["image_base"], int(t["target_off"], 16))
        print(f"  {t['call_at_off']} -> {t['target_off']} (VA {va})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
