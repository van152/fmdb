"""Final micro-checks: remaining getters/setters, unnamed non-constant slots,
STARTING_RECORD table number, full-archive item-level domain validation for all 16 list fields,
election/Cown cross-checks, and known-club L2 anchors."""
import sys, os, struct, json, hashlib
from collections import Counter, defaultdict
sys.path.insert(0, r"D:\tmp2b\fm24\tools\python")
import pefile, capstone, zstandard

EXE = r"D:\tmp2b\fm24\input\editor.exe"
DATA_DIR = os.environ.get("FM24_DB_DIR", r"D:\tmp2b\fm24-db\scratch\data")
MASTER = r"D:\tmp2b\fm24-db\evidence\fm24\reports\editor_schema\master.json"
DB_TABLES = r"D:\tmp2b\fm24-db\evidence\fm24\reports\dbdat_decode\db_tables_big.json"

with open(EXE, "rb") as f:
    PE_BYTES = f.read()
pe = pefile.PE(data=PE_BYTES, fast_load=True)
IB = pe.OPTIONAL_HEADER.ImageBase

def va(fo):
    return IB + pe.get_rva_from_offset(fo)

def fo_from_va(v):
    return pe.get_offset_from_rva(v - IB)

md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

def disasm_func(start_fo, max_bytes=0x600):
    lines = []
    start_va = va(start_fo)
    for ins in md.disasm(PE_BYTES[start_fo:start_fo+max_bytes], start_va):
        fo = ins.address - start_va + start_fo
        extra = ""
        # check 4CC imm
        for op in ins.op_str.split(","):
            op = op.strip()
            if op.startswith("0x") and len(op) == 10:
                val = int(op, 16)
                bs = val.to_bytes(4, "big")
                if all(32 <= b < 127 for b in bs):
                    extra += f"  ; 4CC '{bs.decode()}'"
        if ins.mnemonic in ("call", "jmp") and ins.op_str.startswith("0x"):
            try:
                tva = int(ins.op_str, 16)
                tfo = fo_from_va(tva)
                extra += f"  ; -> 0x{tfo:x}"
                # resolve thunk jmp rel32
                if PE_BYTES[tfo] == 0xe9:
                    rel = struct.unpack_from("<i", PE_BYTES, tfo+1)[0]
                    t2fo = fo_from_va(tva + 5 + rel)
                    extra += f" (thunk->0x{t2fo:x})"
            except Exception:
                pass
        lines.append(f"  0x{fo:x}: {ins.mnemonic:8s} {ins.op_str}{extra}")
        if ins.mnemonic == "ret":
            # stop after a clean ret if followed by cc/nop/int3
            nxt = fo + ins.size
            if PE_BYTES[nxt] in (0xcc, 0x90) or PE_BYTES[nxt:nxt+2] == b"\x66\x90":
                break
    return "\n".join(lines)

# 1. Disassemble remaining small targets
targets = [
    ("CPSL_ITEM_GET_0x1524af0", 0x1524af0, 0x250),
    ("CPSL_SET_0xeac360", 0xeac360, 0x350),
    ("CSCM_SET_0xeaedb0", 0xeaedb0, 0x350),
    ("CLUB_EXTRA_SET_HEAD_0xe57e60", 0xe57e60, 0x900),
    ("EXTRA_DA_DECODER_0x4348ef0", 0x4348ef0, 0x150),
    ("CLUB_GET_KIT_FILTER_0x3ec2f60", 0x3ec2f60, 0x300),
    ("VTAG5_SET_0x42cfa50_CHECK", 0x18b8768, 0),
]

out_lines = []
for name, fo, sz in targets:
    if sz == 0:
        continue
    out_lines.append(f"=== {name} @ 0x{fo:x} (VA 0x{va(fo):x}) ===")
    out_lines.append(disasm_func(fo, sz))

# Check vtable slots for tag 4,5,6,7,37,38 (+0x28 getter, +0x30 setter?)
out_lines.append("=== POLYMORPHIC VTABLES (+0x00..+0x50) ===")
vtables = [
    ("tag4_COMP_BONUS", 0x18b86b8),
    ("tag5_NEXT_SALE", 0x18b8768),
    ("tag6_APP_MONEY", 0x18b8818),
    ("tag7_BUY_BACK", 0x18b8608),
    ("tag9_START_REC", 0x18b9208),
    ("tag16_CUP_PTS", 0x18b9a88),
    ("tag37_EPPP_APP", 0x18b88d8),
    ("tag38_TESTIMONIAL", 0x18b9428),
]
for vname, vfo in vtables:
    slots = []
    for off in range(0, 0x58, 8):
        ptr = struct.unpack_from("<Q", PE_BYTES, vfo + off)[0]
        try:
            tfo = fo_from_va(ptr)
            slots.append(f"+0x{off:02x}=0x{tfo:x}")
        except Exception:
            slots.append(f"+0x{off:02x}=0x{ptr:x}")
    out_lines.append(f"  {vname} (vt 0x{vfo:x}): " + " ".join(slots))

# Check which database table loads into [db + 0x80] (STARTING_RECORD)
out_lines.append("=== CHECK [db + 0x80] INIT IN 0xf025c0..0xf03800 ===")
# In t71, 0xf0296b init'd table 3 into [db+0x10]. Scan for mov [reg+0x80], rax or similar in 0xf01000..0xf05000
for ins in md.disasm(PE_BYTES[0xf01000:0xf06000], va(0xf01000)):
    if "+ 0x80]" in ins.op_str and ins.mnemonic == "mov":
        fo = fo_from_va(ins.address)
        out_lines.append(f"  0x{fo:x}: {ins.mnemonic} {ins.op_str}")
        # dump 15 instructions before
        for ins2 in md.disasm(PE_BYTES[fo-0x60:fo+0x10], va(fo-0x60)):
            fo2 = fo_from_va(ins2.address)
            out_lines.append(f"    ctx 0x{fo2:x}: {ins2.mnemonic} {ins2.op_str}")

# Check ALL references to +0x123 in CLUB_GET (0xe89a00..0xe91e00), CLUB_SET (0xe81000..0xe87000), CLUB_EXTRA_SET (0xe57e60..0xe58900)
# and +0xda in same, and +0xac in TC_GET2 (0x11f0690..0x11f4000), TC_SET2 (0x11f4000..0x11f8000), TC_EXTRA_SET (0x11cf800..0x11d0200)
out_lines.append("=== SEARCH +0x123, +0xda, +0xac IN GETTERS/SETTERS ===")
ranges = [
    ("CLUB_GET", 0xe89a00, 0xe91db0),
    ("CLUB_SET", 0xe81000, 0xe86b54),
    ("CLUB_EXTRA_SET", 0xe57e60, 0xe58b00),
    ("TC_GET2", 0x11f0690, 0x11f3500),
    ("TC_SET2", 0x11f4200, 0x11f6500),
    ("TC_EXTRA_SET", 0x11cf800, 0x11d0400),
    ("CLUB_EXTRA_READER", 0xe5d210, 0xe5ee00),
    ("TC_EXTRA_READER", 0x11d3200, 0x11d4200),
]
for rname, s, e in ranges:
    for ins in md.disasm(PE_BYTES[s:e], va(s)):
        if any(k in ins.op_str for k in ("+ 0x123]", "+ 0xda]", "+ 0xac]")):
            fo = fo_from_va(ins.address)
            out_lines.append(f"  [{rname}] 0x{fo:x}: {ins.mnemonic} {ins.op_str}")

with open(r"D:\tmp2b\fm24-db\scratch\t82\disasm_recon13.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(out_lines))
print(f"Wrote disasm_recon13.txt ({len(out_lines)} lines)")

# 2. Load master.json club.xml list_item_fields for all 16 list fields
with open(MASTER, "r", encoding="utf-8") as f:
    master = json.load(f)
club_fields = master["entities"]["club.xml"]["fields"]
enums = master["enums"]
target_lists = ["Cscm", "CPsL", "Cspb", "Cren", "TCrs", "Tko1", "Tkg1", "Tko2", "Tkg2", "Tko3", "Tkg3", "Csoc", "Camc", "Cbbl", "pcpt"]
print("\n=== MASTER.JSON LIST ITEM SCHEMAS ===")
for i, fld in enumerate(club_fields):
    if fld.get("code") in target_lists:
        print(f"  [{i}] {fld['code']} ({fld.get('name')}): type={fld.get('type')} subfields=")
        for sf in fld.get("list_item_fields", []) or []:
            er = sf.get("enum_ref")
            es = enums.get(er) if er else None
            ev_info = f"enum_vals={len(es['values'])}" if isinstance(es, dict) and 'values' in es else (f"enum_len={len(es)}" if es else "enum_ref=None")
            print(f"      {sf.get('code')} ({sf.get('name')}): type={sf.get('type')} min={sf.get('min_value')} max={sf.get('max_value')} enum_ref={er} ({ev_info}) target={sf.get('target_entity') or sf.get('db_type')}")

# 3. Check db_tables_big.json for club, comp, person, stage_name table numbers and counts
with open(DB_TABLES, "r", encoding="utf-8") as f:
    dbt = json.load(f)
print("\n=== DB_TABLES_BIG SUMMARY (matching club/comp/person/stage/record) ===")
tables_list = dbt.get("tables", dbt) if isinstance(dbt, dict) else dbt
if isinstance(tables_list, dict):
    for k, v in tables_list.items():
        s = str(v)[:180]
        if any(w in s.lower() for w in ("club", "comp", "person", "people", "stage", "record")):
            print(f"  {k}: {s}")
elif isinstance(tables_list, list):
    for v in tables_list:
        s = str(v)[:180]
        if any(w in s.lower() for w in ("club", "comp", "person", "people", "stage", "record")):
            print(f"  {s}")

# 4. Decompress table_extra_3 (client+server), table_3 (server) for ordinal->UID + club name, table_25 (comp) for comp ordinal/UID, etc.
def load_fmf_member(fmf_path, member_name):
    with open(fmf_path, "rb") as f:
        data = f.read()
    # FMF container: 0x02 0x01 'fmf.' ... let's use exact FMF TOC layout (same as recon11)
    assert data[:2] == b"\x02\x01" and data[2:6] == b"fmf."
    toc_off = struct.unpack_from("<I", data, 9)[0] + 17
    # Wait: check recon11's exact FMF reader! Let's read compressed TOC zstd stream
    # Find zstd magic 28 b5 2f fd at toc_off or use standard offset
    if data[toc_off:toc_off+4] != b"\x28\xb5\x2f\xfd":
        # standard FM24 FMF: header 9 bytes + 4B toc_off + 4B unknown? Let's locate cleanly
        toc_off = struct.unpack_from("<I", data, 9)[0] + 13
    dctx = zstandard.ZstdDecompressor()
    # Find exact FMF TOC via searching from header offset
    toc = dctx.stream_reader(data[toc_off:]).read()
    # Parse TOC recursively to find member_name
    pos = 0
    # skip root 3B version/unknown? Actually let's check recon11 directly or parse properly
    return None

# Import our own recon11's FMF extractor? No, write clean self-contained FMF parser verified against known offsets
def extract_fmf_members(fmf_path, want_names):
    with open(fmf_path, "rb") as f:
        raw = f.read()
    assert raw[:6] == b"\x02\x01fmf."
    # header: 0..9, [9:13] u32 toc_offset from 17? Wait check!
    off_rel = struct.unpack_from("<I", raw, 9)[0]
    toc_start = off_rel + 17
    if raw[toc_start:toc_start+4] != b"\x28\xb5\x2f\xfd":
        toc_start = off_rel + 13
    if raw[toc_start:toc_start+4] != b"\x28\xb5\x2f\xfd":
        # FM24 FMF: [9:13] is file_data_size, data starts at 17, toc is at 17+file_data_size? Wait let's test
        raise RuntimeError(f"Unexpected TOC magic at {toc_start}: {raw[toc_start:toc_start+4].hex()}")
    dctx = zstandard.ZstdDecompressor()
    toc = dctx.stream_reader(raw[toc_start:]).read()
    # Walk FMF directory tree
    pos = 0
    def read_u16():
        nonlocal pos
        v = struct.unpack_from("<H", toc, pos)[0]; pos += 2; return v
    def read_u32():
        nonlocal pos
        v = struct.unpack_from("<I", toc, pos)[0]; pos += 4; return v
    def read_str():
        nonlocal pos
        n = read_u32()
        # FM UTF-16LE string: 2*n bytes (plus flag?) Let's check!
        s = toc[pos:pos+n*2].decode("utf-16-le"); pos += n*2; return s
    return raw, toc

# Wait: instead of guessing FMF string encoding, peek at recon11's FMF loader (we wrote it 15 min ago!)
with open(r"D:\tmp2b\fm24-db\scratch\t82\recon11_profile_all.py", "r", encoding="utf-8") as f:
    r11 = f.read()
# Extract lines 1-90 of recon11 just to check exact FMF header math
print("\n[recon11 header check]:")
for line in r11.splitlines()[:45]:
    if "def " in line or "FMF" in line or "toc" in line.lower() or "tad" in line.lower() or "zstd" in line.lower():
        print(" ", line)
