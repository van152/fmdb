import json, struct
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

ROOT = Path(r"D:\tmp2b\fm24-db")
# 1. Inspect LEDGER.json for t57/t63/t74/t76b/t76c/t79
ledger = json.loads((ROOT / "scratch/t01/LEDGER.json").read_text(encoding="utf-8"))
entries = ledger if isinstance(ledger, list) else ledger.get("entries", [])
out = ["=== LEDGER RELEVANT ENTRIES ==="]
for e in entries:
    s = json.dumps(e, ensure_ascii=False)
    if any(k in s.lower() for k in ("t57", "t63", "t74", "t76", "award", "language", "weather", "derby", "media", "rdui", "e115", "e118")):
        out.append(s[:600])

# 2. Check [db+offset] -> table_id binding via editor.exe!
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
def va_to_fo(va): return rva_to_fo(va - image_base)

md = Cs(CS_ARCH_X86, CS_MODE_64)
def dis_brief(name, fo, n=35):
    out.append(f"\n=== {name} fo={fo:#x} va={fo_to_va(fo):#x} ===")
    va0 = fo_to_va(fo)
    cnt = 0
    for ins in md.disasm(data[fo:fo+256], va0):
        ifo = fo + (ins.address - va0)
        note = ""
        if ins.mnemonic in ("call", "jmp") and ins.op_str.startswith("0x"):
            try:
                tfo = va_to_fo(int(ins.op_str, 16))
                note = f" ; -> fo={tfo:#x}"
            except Exception: pass
        out.append(f"  {ifo:#x}  {ins.mnemonic:8s} {ins.op_str}{note}")
        cnt += 1
        if cnt >= n or ins.mnemonic == "ret":
            break

# Trace db_context_clean table object constructors & fixup resolvers
for name, fo in [
    ("fixup_0xf7e820_AWci", 0xf7e820),
    ("fixup_0xf7f030_AWni", 0xf7f030),
    ("fixup_0xf7e610_AWmi", 0xf7e610),
    ("fixup_0xf7ed30_AW68", 0xf7ed30),
    ("fixup_0x3bf3190", 0x3bf3190),
    ("fixup_0x3bf4a90", 0x3bf4a90),
    ("fixup_0x3bf5e90", 0x3bf5e90),
    ("fixup_0x3bf5fd0", 0x3bf5fd0),
    ("fixup_0x3bf6ec0", 0x3bf6ec0),
    ("fixup_0x3bf9220", 0x3bf9220),
    ("load_f4e4b0_table_loader", 0xf4e4b0),
    ("AWsh_global_check_0x1a01b00", 0xf026c0),
]:
    dis_brief(name, fo, 35)

# Also check AWsh global pointer in 0x43380aa: mov rax, qword ptr [rip - 0x29435c1]
ins_va = fo_to_va(0x43380aa) + 7
awsh_glob_va = ins_va - 0x29435c1
out.append(f"\nAWsh global VA = {awsh_glob_va:#x}")
# Check where this global VA is written/referenced in 0xf026c0 or nearby!
# Scan 0xf026c0..0xf03700 for RIP-relative refs to globals and [r14+off] table allocations!
out.append("\n=== DB_CONTEXT (0xf026c0..0xf03600) table-id / global bindings ===")
va0 = fo_to_va(0xf026c0)
last_mov_edx = None
last_store_r14 = None
for ins in md.disasm(data[0xf026c0:0xf03600], va0):
    ifo = 0xf026c0 + (ins.address - va0)
    if "r14" in ins.op_str or "edx" in ins.op_str or "ecx" in ins.op_str or "rip" in ins.op_str or ins.mnemonic == "call":
        # check if rip ref matches awsh_glob_va
        extra = ""
        if "rip" in ins.op_str and ins.mnemonic in ("mov", "lea"):
            try:
                # parse [rip + 0x...] or [rip - 0x...]
                s = ins.op_str
                if "rip + 0x" in s:
                    disp = int(s.split("rip + 0x")[1].split("]")[0], 16)
                    target = ins.address + ins.size + disp
                elif "rip - 0x" in s:
                    disp = int(s.split("rip - 0x")[1].split("]")[0], 16)
                    target = ins.address + ins.size - disp
                else:
                    target = None
                if target == awsh_glob_va:
                    extra = "  <<< AWsh GLOBAL!"
            except Exception:
                pass
        if extra or "[r14" in ins.op_str or (ins.mnemonic == "mov" and ins.op_str.startswith(("edx, ", "r8d, "))):
            out.append(f"  {ifo:#x}  {ins.mnemonic:8s} {ins.op_str}{extra}")

Path(r"D:\tmp2b\fm24-db\scratch\t83\ledger_and_dbmap.txt").write_text("\n".join(out), encoding="utf-8")
print("Wrote ledger_and_dbmap.txt")
