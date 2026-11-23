import json, struct, os, sys
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64

EXE = Path(r"D:\tmp2b\fm24\input\editor.exe")
data = EXE.read_bytes()

# Parse PE32+
pe_off = struct.unpack_from("<I", data, 0x3C)[0]
num_sec = struct.unpack_from("<H", data, pe_off + 6)[0]
opt_sz = struct.unpack_from("<H", data, pe_off + 20)[0]
image_base = struct.unpack_from("<Q", data, pe_off + 24 + 24)[0]
pdata_rva, pdata_sz = struct.unpack_from("<II", data, pe_off + 24 + 112 + 3 * 8)

sections = []
sec_off = pe_off + 24 + opt_sz
for i in range(num_sec):
    o = sec_off + i * 40
    name = data[o:o+8].rstrip(b"\x00").decode("ascii", "replace")
    vsz, va, rsz, ra = struct.unpack_from("<IIII", data, o + 8)
    sections.append((name, va, max(vsz, rsz), ra, rsz))

def rva_to_fo(rva):
    for _, va, vsz, ra, rsz in sections:
        if va <= rva < va + rsz:
            return ra + (rva - va)
    raise ValueError(f"rva {rva:#x}")

def fo_to_va(fo):
    for _, va, vsz, ra, rsz in sections:
        if ra <= fo < ra + rsz:
            return image_base + va + (fo - ra)
    raise ValueError(f"fo {fo:#x}")

def va_to_fo(va):
    return rva_to_fo(va - image_base)

# Parse .pdata
pdata_fo = rva_to_fo(pdata_rva)
funcs = []
for o in range(pdata_fo, pdata_fo + pdata_sz, 12):
    b, e, u = struct.unpack_from("<III", data, o)
    if b == 0 and e == 0:
        break
    funcs.append((b, e))

import bisect
func_starts = [b for b, _ in funcs]

def find_func_fo(fo):
    rva = fo_to_va(fo) - image_base
    idx = bisect.bisect_right(func_starts, rva) - 1
    if idx >= 0:
        b, e = funcs[idx]
        if b <= rva < e:
            return rva_to_fo(b), rva_to_fo(e)
    return None

md = Cs(CS_ARCH_X86, CS_MODE_64)
md.detail = False

def fmt_4cc(v):
    if 0x20202020 <= v <= 0x7e7e7e7e:
        bs = struct.pack(">I", v)
        if all(32 <= c < 127 for c in bs):
            return bs.decode("ascii")
    return None

def dis_func(name, fo, max_bytes=4096):
    bounds = find_func_fo(fo)
    if bounds:
        s, e = bounds
        e = min(e, s + max_bytes)
    else:
        s = fo
        e = fo + min(max_bytes, 512)
    out = [f"=== {name} fo={s:#x}..{e:#x} va={fo_to_va(s):#x} ==="]
    va0 = fo_to_va(s)
    for ins in md.disasm(data[s:e], va0):
        ifo = s + (ins.address - va0)
        note = ""
        # check 4CC imm
        for tok in ins.op_str.replace(",", " ").split():
            if tok.startswith("0x") and len(tok) in (9, 10):
                try:
                    v = int(tok, 16)
                    cc = fmt_4cc(v)
                    if cc:
                        note += f" ; '{cc}'"
                except Exception:
                    pass
        if ins.mnemonic in ("call", "jmp") and ins.op_str.startswith("0x"):
            try:
                tva = int(ins.op_str, 16)
                tfo = va_to_fo(tva)
                note += f" ; -> fo={tfo:#x}"
            except Exception:
                pass
        out.append(f"  {ifo:#x}  {ins.mnemonic:8s} {ins.op_str}{note}")
        if not bounds and ins.mnemonic == "ret":
            break
    return "\n".join(out)

targets = [
    ("Mtyp_helper_45f25b0", 0x45f25b0, 4096),
    ("Mcli_item_154dc00", 0x154dc00, 4096),
    ("Mtyp_item_4381840", 0x4381840, 2048),
    ("AWsh_helper_4338030", 0x4338030, 3072),
    ("t79_load_tables_f5167e", 0xf5167e, 8192),
    ("prompt_helper_151d2e0", 0x151d2e0, 512),
    ("prompt_helper_151d710", 0x151d710, 512),
    ("prompt_helper_15211a0", 0x15211a0, 512),
    ("prompt_helper_4339e80", 0x4339e80, 512),
    ("prompt_helper_433bbc0", 0x433bbc0, 512),
    ("prompt_helper_4342940", 0x4342940, 512),
]

parts = []
for name, fo, mb in targets:
    parts.append(dis_func(name, fo, mb))

Path(r"D:\tmp2b\fm24-db\scratch\t83\dis_remaining.txt").write_text("\n\n".join(parts), encoding="utf-8")

# Also decode all [db+off] assignments in f51xxx and 0xf026c0, and check enums['foms'] in master.json
master = json.loads(Path(r"D:\tmp2b\fm24-db\evidence\fm24\reports\editor_schema\master.json").read_text(encoding="utf-8"))
enums = master.get("enums", {})
lines = []
for k in ["foms", "awty", "awdr", "awrt", "awnp", "awpo", "awsr", "awsc", "awvf", "awrb", "awbr", "awss", "awap"]:
    if k in enums:
        lines.append(f"enum[{k}]: {json.dumps(enums[k], ensure_ascii=False)}")
# Also check all enum keys referenced by our 5 entities
ent_keys = ["award.xml", "language.xml", "weather.xml", "derby.xml", "media source.xml"]
for ek in ent_keys:
    ent = master["entities"][ek]
    lines.append(f"\n--- Entity {ek} ({len(ent['fields'])} fields) enum refs ---")
    for f in ent["fields"]:
        ef = f.get("enum") or f.get("enum_name") or f.get("enum_id") or f.get("list")
        if ef and isinstance(ef, str):
            lines.append(f"  {f.get('id')} ({f.get('type')}): ref={ef} -> in master.enums={ef in enums}")
            if ef in enums:
                lines.append(f"    {json.dumps(enums[ef], ensure_ascii=False)[:300]}")
        elif f.get("type") in ("enum", "bitmask", "flags", "list") or f.get("enum_values"):
            lines.append(f"  {f.get('id')} ({f.get('type')}): keys={list(f.keys())}")

# Also search master.json for any field in these 5 entities that references enum or flags
for ek in ent_keys:
    for f in master["entities"][ek]["fields"]:
        for k, v in f.items():
            if k not in ("id", "name", "type", "min", "max", "default", "read_only", "optional", "hidden"):
                lines.append(f"  EXTRA {ek}.{f.get('id')}.{k} = {str(v)[:200]}")

Path(r"D:\tmp2b\fm24-db\scratch\t83\enums_extra.txt").write_text("\n".join(lines), encoding="utf-8")
print("Wrote dis_remaining.txt and enums_extra.txt")
