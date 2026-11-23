"""Scan all code for `mov r64,[rip+d]` -> `mov r64,[r64+0x80]` dbctx-deref pattern."""
import pefile, capstone, re, sys
from collections import Counter

PE = r"D:\tmp2b\fm24\input\editor.exe"
pe = pefile.PE(PE, fast_load=True)
raw = open(PE, "rb").read()
IB = pe.OPTIONAL_HEADER.ImageBase

hits = Counter()
ctx = Counter()
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
md.detail = True
RIPREL = re.compile(r"^(r[a-z0-9]+), qword ptr \[rip \+ (0x[0-9a-f]+)\]$")
DEREF = re.compile(r"^(r[a-z0-9]+), qword ptr \[\1 \+ 0x80\]$")

for s in pe.sections:
    if s.PointerToRawData == 0 or s.SizeOfRawData == 0:
        continue
    name = s.Name.rstrip(b"\x00").decode()
    if name not in (".reloc", ".text"):
        continue
    fo, va0, sz = s.PointerToRawData, s.VirtualAddress, min(s.Misc_VirtualSize, s.SizeOfRawData)
    insns = list(md.disasm(raw[fo:fo+sz], IB + va0))
    for i, ins in enumerate(insns):
        m = RIPREL.match(ins.op_str)
        if not m:
            continue
        reg, disp = m.group(1), int(m.group(2), 16)
        tgt = ins.address + ins.size + disp
        # look ahead up to 3 insns for [reg+0x80] deref
        ok = False
        for j in range(i+1, min(i+4, len(insns))):
            if DEREF.match(insns[j].op_str):
                ok = True
                break
            if insns[j].mnemonic in ("call", "jmp", "ret") or "rip" in insns[j].op_str:
                break
        if ok:
            hits[tgt] += 1
            ctx[(ins.address)] = tgt

print("deref-globals ([g] -> [g+0x80]):", len(hits))
for g, n in sorted(hits.items()):
    print(f"  0x{g:x}  x{n}")

# also: any rip-rel load followed by +0x78 deref (variant offset)
h78 = Counter()
for s in pe.sections:
    if s.PointerToRawData == 0 or s.SizeOfRawData == 0:
        continue
    name = s.Name.rstrip(b"\x00").decode()
    if name not in (".reloc", ".text"):
        continue
    fo, va0, sz = s.PointerToRawData, s.VirtualAddress, min(s.Misc_VirtualSize, s.SizeOfRawData)
    insns = list(md.disasm(raw[fo:fo+sz], IB + va0))
    for i, ins in enumerate(insns):
        m = RIPREL.match(ins.op_str)
        if not m:
            continue
        reg, disp = m.group(1), int(m.group(2), 16)
        tgt = ins.address + ins.size + disp
        for j in range(i+1, min(i+4, len(insns))):
            m2 = re.match(rf"^(r[a-z0-9]+), qword ptr \[{reg} \+ (0x[0-9a-f]+)\]$", insns[j].op_str)
            if m2 and m2.group(2) in ("0x78", "0x88", "0x90"):
                h78[(tgt, m2.group(2))] += 1
            if insns[j].mnemonic in ("call", "jmp", "ret") or "rip" in insns[j].op_str:
                break
print()
print("variant offsets 0x78/0x88/0x90:")
for (g, off), n in sorted(h78.items()):
    print(f"  0x{g:x} +{off}  x{n}")
