import json, os, struct, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(r"D:\tmp2b\fm24-db")
EXE = Path(r"D:\tmp2b\fm24\input\editor.exe")
data = EXE.read_bytes()

pe_off = struct.unpack_from("<I", data, 0x3C)[0]
num_sec = struct.unpack_from("<H", data, pe_off + 6)[0]
opt_sz = struct.unpack_from("<H", data, pe_off + 20)[0]
image_base = struct.unpack_from("<Q", data, pe_off + 24 + 24)[0]
sections = []
sec_off = pe_off + 24 + opt_sz
for i in range(num_sec):
    o = sec_off + i * 40
    name = data[o:o+8].rstrip(b"\x00").decode("ascii", "replace")
    vsz, va, rsz, ra = struct.unpack_from("<IIII", data, o + 8)
    sections.append((name, va, max(vsz, rsz), ra, rsz))

def fo_to_va(fo):
    for _, va, vsz, ra, rsz in sections:
        if ra <= fo < ra + rsz: return image_base + va + (fo - ra)
    raise ValueError(hex(fo))

def va_to_fo(va):
    rva = va - image_base
    for _, va0, vsz, ra, rsz in sections:
        if va0 <= rva < va0 + rsz: return ra + (rva - va0)
    raise ValueError(hex(va))

md = Cs(CS_ARCH_X86, CS_MODE_64)

# 1. Exact DB_CONTEXT table_id for EVERY [r14+off] by looking at the `call 0xff9910` (DATABASE_TABLE ctor) args!
print("=== DB_CONTEXT DATABASE_TABLE ctor (0xff9910) calls ===")
va0 = fo_to_va(0xf026c0)
ins_list = list(md.disasm(data[0xf026c0:0xf09500], va0))
for i, ins in enumerate(ins_list):
    if ins.mnemonic == "call" and ins.op_str.startswith("0x"):
        try:
            tfo = va_to_fo(int(ins.op_str, 16))
        except Exception:
            continue
        if tfo == 0xff9910:
            # look back 6 insns for edx (tid) and forward 30 insns for mov [r14+off], rdi
            tid_s = "?"
            for j in range(max(0, i-8), i):
                if ins_list[j].mnemonic == "xor" and ins_list[j].op_str == "edx, edx":
                    tid_s = "0"
                elif ins_list[j].mnemonic == "mov" and ins_list[j].op_str.startswith("edx, "):
                    tid_s = str(int(ins_list[j].op_str.split(", ")[1], 0))
            off_s = "?"
            store_fo = 0
            for j in range(i+1, min(len(ins_list), i+65)):
                if ins_list[j].mnemonic == "mov" and ins_list[j].op_str.startswith("qword ptr [r14") and ins_list[j].op_str.endswith(", rdi"):
                    off_s = ins_list[j].op_str
                    store_fo = 0xf026c0 + (ins_list[j].address - va0)
                    break
            cfo = 0xf026c0 + (ins.address - va0)
            if off_s != "?" and any(x in off_s for x in ("[r14]", "+ 8]", "+ 0x10]", "+ 0x18]", "+ 0x20]", "+ 0x28]", "+ 0x48]", "+ 0x50]", "+ 0x58]", "+ 0x60]", "+ 0x68]", "+ 0x80]", "+ 0x90]", "+ 0x98]", "+ 0xa0]", "+ 0xb0]", "+ 0xc0]", "+ 0xc8]")):
                print(f"  ctor@{cfo:#x} tid={tid_s:>3s} -> store@{store_fo:#x}: {off_s}")

# Also search for any write to [r14 + 0xc0] in 0xf026c0..0xf0a500 or anywhere nearby!
print("\n=== Searching [r14 + 0xc0] or [rcx + 0xc0] in 0xf026c0..0xf0a500 ===")
for ins in ins_list:
    if "+ 0xc0]" in ins.op_str:
        ifo = 0xf026c0 + (ins.address - va0)
        print(f"  {ifo:#x}: {ins.mnemonic} {ins.op_str}")

# 2. Vectorized search in .text for RIP-relative reference to 0x141b600f0 (AWsh global)!
import numpy as np
_, t_va, _, t_ra, t_rsz = sections[0]
# A RIP-relative disp32 at byte offset p in .text points to target_va iff:
#   (image_base + t_va + p + 4) + int32(text[p:p+4]) == target_va
# => int32(text[p:p+4]) + p == target_va - image_base - t_va - 4
target_va = 0x141b600f0
want = (target_va - image_base - t_va - 4) & 0xFFFFFFFF
text_u8 = np.frombuffer(data, dtype=np.uint8, offset=t_ra, count=t_rsz)
# check all 4 alignments
hits = []
for align in range(4):
    n = (t_rsz - align) // 4
    vals = text_u8[align:align + n*4].view("<i4")
    pos = np.arange(n, dtype=np.int64) * 4 + align
    m = ((vals.astype(np.int64) + pos) & 0xFFFFFFFF) == want
    for idx in np.nonzero(m)[0]:
        p = int(pos[idx])
        fo = t_ra + p
        # check instruction starting 1..4 bytes before p
        for back in (3, 4, 2, 1):
            try:
                ins = next(md.disasm(data[fo-back:fo+8], fo_to_va(fo-back), 1))
                if ins.size == back + 4 and "rip" in ins.op_str:
                    hits.append((fo - back, ins.mnemonic, ins.op_str))
                    break
            except Exception:
                pass
print(f"\n=== ALL .text refs to AWsh global {target_va:#x} ({len(hits)} hits) ===")
for fo, mn, op in hits[:25]:
    print(f"  {fo:#x}: {mn:8s} {op}")

# Also check what is at 0x141b600f0 (is it in .data/.bss?) and check surrounding writes near the first write!
for fo, mn, op in hits:
    if op.startswith("qword ptr [rip"):
        print(f"\n  Context around WRITE {fo:#x}:")
        v = fo_to_va(fo - 32)
        for ins in md.disasm(data[fo-32:fo+32], v):
            ifo = (fo - 32) + (ins.address - v)
            print(f"    {ifo:#x}: {ins.mnemonic:8s} {ins.op_str}")
        break

# 3. Check LANGUAGE::get (0x1038a00) for Lfam/Lgro/Lsub clamping/suppression and MEDIA_SOURCE::get for Mdlp/Mtyp/Mper/Mscp/Msty
print("\n=== CHECK LANGUAGE::get (Lfam/Lgro/Lsub/Linf/Ldff/Lnat) ===")
for label, start, length in [
    ("LANGUAGE::get_all", 0x1038a00, 0x520),
]:
    v = fo_to_va(start)
    for ins in md.disasm(data[start:start+length], v):
        ifo = start + (ins.address - v)
        if any(k in ins.op_str for k in ("0x4c", "0x64626e6d", "+ 0x3", "+ 0x2", "0x18")):
            print(f"  {ifo:#x}: {ins.mnemonic:8s} {ins.op_str}")
