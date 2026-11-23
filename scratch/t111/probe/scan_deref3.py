"""Byte-pattern scan: mov r64,[rip+d32] {gap<=8} mov r64,[r64+0x80]  -> collect globals."""
import pefile, re, sys
from collections import Counter

PE = r"D:\tmp2b\fm24\input\editor.exe"
pe = pefile.PE(PE, fast_load=True)
raw = open(PE, "rb").read()
IB = pe.OPTIONAL_HEADER.ImageBase

# offset -> VA map
segs = []
for s in pe.sections:
    if s.PointerToRawData and s.SizeOfRawData:
        segs.append((s.PointerToRawData, s.PointerToRawData + s.SizeOfRawData,
                     IB + s.VirtualAddress, s.Name.rstrip(b"\x00").decode()))

def off_to_va(off):
    for lo, hi, va, name in segs:
        if lo <= off < hi:
            return va + (off - lo), name
    return None, None

# mov r64,[rip+d32]: REX(48|49|4c) 8B modrm(mod=00,rm=101) d32
# mov r64,[r64+0x80]: REX(48|49|4c) 8B modrm(mod=10) 80 00 00 00
pat = re.compile(
    rb"[\x48\x49\x4c]\x8b[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]...."   # rip-rel load
    rb".{0,8}?"
    rb"[\x48\x49\x4c]\x8b[\x80-\x8f]\x80\x00\x00\x00", re.S)        # [reg+0x80]

hits = Counter(); sites = {}
for m in pat.finditer(raw):
    off1 = m.start()
    va, name = off_to_va(off1)
    if va is None or name not in (".rdata", ".reloc", ".text"):
        continue
    disp = int.from_bytes(raw[off1+4:off1+8], "little", signed=True)
    tgt = va + 8 + disp
    hits[tgt] += 1
    sites.setdefault(tgt, []).append(va)

print("candidate globals ([g] then [g+0x80]):", len(hits))
for g, n in sorted(hits.items()):
    if 0x141800000 <= g <= 0x141C00000:
        print(f"  0x{g:x}  x{n}  sites={[hex(a) for a in sites[g][:4]]}")
