import json, struct
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(r"D:\tmp2b\fm24-db")
# 1. Inspect t79 held & L3 grading rules (enum 0, suppressed dates, etc.)
fm79 = json.loads((ROOT / "scratch/t79/out/field_map.json").read_text(encoding="utf-8"))
print("=== t79 HELD FIELDS & 0-LIVE L3 FIELDS ===")
for tbl in ("stadium_21", "team_24"):
    for f in fm79[tbl]["schema_fields"]:
        g = f["grade"]
        if g == "held" or (g == "L3" and f.get("domain", {}).get("live") == 0) or (g == "L3" and "allowed_enum" in f.get("domain", {})):
            print(f"  {tbl}.{f['field']} ({f['schema_type']}) grade={g}: hold={f.get('hold_reason','')[:120]} dom={str(f.get('domain'))[:160]}")

# 2. Check all [r14+off] table_id bindings in 0xf026c0..0xf04910 AND where 0x141b600f0 (AWsh global) is referenced
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
    vsz, va, rsz, ra = struct.unpack_from("<IIII", data, o + 8)
    sections.append((va, max(vsz, rsz), ra, rsz))
def rva_to_fo(rva):
    for va, vsz, ra, rsz in sections:
        if va <= rva < va + rsz: return ra + (rva - va)
    raise ValueError(hex(rva))
def fo_to_va(fo):
    for va, vsz, ra, rsz in sections:
        if ra <= fo < ra + rsz: return image_base + va + (fo - ra)
    raise ValueError(hex(fo))

md = Cs(CS_ARCH_X86, CS_MODE_64)
va0 = fo_to_va(0xf026c0)
print("\n=== DB_CONTEXT [r14+off] -> table_id (0xf026c0..0xf04910) ===")
cur_tid = 0  # first one uses xor edx, edx at 0xf026f0
for ins in md.disasm(data[0xf026c0:0xf04910], va0):
    ifo = 0xf026c0 + (ins.address - va0)
    if ins.mnemonic == "xor" and ins.op_str == "edx, edx":
        cur_tid = 0
    elif ins.mnemonic == "mov" and ins.op_str.startswith("edx, ") and ins.op_str != "edx, 0x18" and ins.op_str != "edx, 0x30":
        try:
            cur_tid = int(ins.op_str.split(", ")[1], 0)
        except Exception:
            pass
    elif ins.mnemonic == "mov" and ins.op_str.startswith("qword ptr [r14") and ins.op_str.endswith(", rdi"):
        print(f"  {ifo:#x}: {ins.op_str:28s} <- tid={cur_tid}")

# Also search 0xf026c0..0xf09000 for RIP ref to 0x141b600f0 (AWsh global) or scan .text for it
target_va = 0x141b600f0
print(f"\n=== Scanning DB_CONTEXT/init for AWsh global {target_va:#x} ===")
# Search in .text (section 0) for 48 89 xx / 48 8b xx [rip+disp32] pointing to 0x141b600f0
va_s, vsz_s, ra_s, rsz_s = sections[0]
# Fast byte scan for target_va - (rip)
base_va = image_base + va_s
text = data[ra_s:ra_s+rsz_s]
hits = []
# Check common opcodes: 48 8b 05, 48 89 05, 48 89 3d, 48 8b 0d, 4c 8b ..., etc.
# Actually scan all occurrences of 0x141b600f0 via sliding disp32 check? Too slow in Python over 30MB; instead check 0xf026c0..0xf0a000 and 0xf40000..0xf60000!
for start_fo, end_fo in [(0xf026c0, 0xf0a500), (0xf40000, 0xf58000), (0x3ba0000, 0x3bb5000)]:
    v0 = fo_to_va(start_fo)
    for ins in md.disasm(data[start_fo:end_fo], v0):
        if "rip" in ins.op_str:
            s = ins.op_str
            try:
                if "rip + 0x" in s:
                    t = ins.address + ins.size + int(s.split("rip + 0x")[1].split("]")[0], 16)
                elif "rip - 0x" in s:
                    t = ins.address + ins.size - int(s.split("rip - 0x")[1].split("]")[0], 16)
                else:
                    continue
                if t == target_va:
                    ifo = start_fo + (ins.address - v0)
                    print(f"  HIT {ifo:#x}: {ins.mnemonic} {ins.op_str}")
            except Exception:
                pass
