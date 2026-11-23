import pefile, capstone, re
from collections import Counter
PE = r"D:\tmp2b\fm24\input\editor.exe"
pe = pefile.PE(PE, fast_load=True)
raw = open(PE, "rb").read()
IB = pe.OPTIONAL_HEADER.ImageBase
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
RIPREL = re.compile(r"^(r[a-z0-9]+), qword ptr \[rip \+ (0x[0-9a-f]+)\]$")
DEREF = re.compile(r"^(r[a-z0-9]+), qword ptr \[\1 \+ 0x80\]$")
hits = Counter(); sites = {}
tot = ripn = 0
for s in pe.sections:
    if s.PointerToRawData == 0 or s.SizeOfRawData == 0:
        continue
    name = s.Name.rstrip(b"\x00").decode()
    if name not in (".rdata", ".reloc", ".text"):
        continue
    fo, va0, sz = s.PointerToRawData, s.VirtualAddress, min(s.Misc_VirtualSize, s.SizeOfRawData)
    insns = list(md.disasm(raw[fo:fo+sz], IB + va0))
    tot += len(insns)
    for i, ins in enumerate(insns):
        m = RIPREL.match(ins.op_str)
        if not m:
            continue
        ripn += 1
        reg, disp = m.group(1), int(m.group(2), 16)
        tgt = ins.address + ins.size + disp
        for j in range(i+1, min(i+4, len(insns))):
            if DEREF.match(insns[j].op_str):
                hits[tgt] += 1
                sites.setdefault(tgt, []).append(ins.address)
                break
            if insns[j].mnemonic in ("call", "ret") or ("[rip" in insns[j].op_str):
                break
print("insns:", tot, "riprel:", ripn, "deref-globals:", len(hits))
for g, n in sorted(hits.items()):
    print(f"  0x{g:x}  x{n}  sites={[hex(a) for a in sites[g][:3]]}")
