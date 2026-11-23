"""Scan whole image: movzx r32, word [rip+d] followed by cmp against imm 0xDC0-0xE20."""
import pefile, re, sys
from collections import Counter

PE = r"D:\tmp2b\fm24\input\editor.exe"
pe = pefile.PE(PE, fast_load=True)
raw = open(PE, "rb").read()
IB = pe.OPTIONAL_HEADER.ImageBase
segs = []
for s in pe.sections:
    if s.PointerToRawData and s.SizeOfRawData:
        segs.append((s.PointerToRawData, s.PointerToRawData + s.SizeOfRawData, IB + s.VirtualAddress, s.Name.rstrip(b"\x00").decode()))
def off_to_va(off):
    for lo, hi, va, name in segs:
        if lo <= off < hi:
            return va + (off - lo), name
    return None, None

# movzx r32, word ptr [rip+d32]: 0F B7 modrm(mod=00,rm=101) d32
mvzx = re.compile(rb"\x0f\xb7[\x05\x0d\x15\x1d\x25\x2d\x35\x3d]....", re.S)
# cmp variants against imm: 3D id32 (cmp eax), 81 F8+r id32 (cmp r32), 66 3D iw, 66 81 F8+r iw
cmps = re.compile(rb"(?:\x3d....|\x81[\xf8-\xff]....|\x66\x3d..|\x66\x81[\xf8-\xff]..)", re.S)

hits = {}
for m in mvzx.finditer(raw):
    va, name = off_to_va(m.start())
    if va is None or name not in (".rdata", ".reloc", ".text"):
        continue
    disp = int.from_bytes(raw[m.start()+3:m.start()+7], "little", signed=True)
    tgt = va + 7 + disp
    window = raw[m.end():m.end()+16]
    for c in cmps.finditer(window):
        b = window[c.start():c.end()]
        if c.start() > 6:   # must be close (≤6 bytes gap)
            break
        if len(b) == 6 and b[0] in (0x3D,) or (len(b) == 6 and b[0] == 0x81):
            imm = int.from_bytes(b[2:6], "little")
        elif len(b) == 4 and b[0] == 0x66 and b[1] == 0x3D:
            imm = int.from_bytes(b[2:4], "little")
        elif len(b) == 5 and b[0] == 0x66 and b[1] == 0x81:
            imm = int.from_bytes(b[3:5], "little")
        else:
            continue
        if 0x0DC0 <= imm <= 0x0E20:
            hits.setdefault(tgt, set()).add(imm)
            break

print("version-gate globals (imm 0xDC0-0xE20):", len(hits))
for g, imms in sorted(hits.items()):
    if 0x141B00000 <= g <= 0x141C00000:
        print(f"  0x{g:x}  imms={[hex(i) for i in sorted(imms)]}")
