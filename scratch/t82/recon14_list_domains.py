"""Full-archive item-level domain validation for ALL 16 list fields in table_extra_3.dat,
plus election/Cown invariants, extra+0xa0[0..5] dates, known-club L2 checks,
STARTING_RECORD global table identification, and unnamed slot (+0x123/+0xda/base+0xac) scan."""
import json, os, struct, sys
from collections import Counter, defaultdict
from pathlib import Path
import numpy as np
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import zstandard as zstd
import pefile, capstone

ROOT = Path(r'D:\tmp2b\fm24-db')
DATA = Path(os.environ.get('FM24_DB_DIR', ROOT / 'scratch/data'))
EXE = Path(r'D:\tmp2b\fm24\input\editor.exe')
HEAD = bytes.fromhex('03017461642ef10d')

# --- 1. Master.json list_item_fields & t71 L3 exclusion check ---
master = json.loads((ROOT / 'evidence/fm24/reports/editor_schema/master.json').read_bytes())
club_fields = master['entities']['club.xml'][0]['fields']
enums = master['enums']
target_lists = ['Cscm', 'CPsL', 'Cspb', 'Cren', 'TCrs',
                'Tko1', 'Tkg1', 'Tko2', 'Tkg2', 'Tko3', 'Tkg3',
                'Csoc', 'Camc', 'Cbbl', 'pcpt']
print('=== 1. MASTER.JSON LIST SCHEMAS ===')
for i, f in enumerate(club_fields):
    if f['field'] in target_lists:
        sub = f.get('fields') or f.get('list_item_fields') or []
        print(f"  [{i:3d}] {f['field']} ({f.get('name')}): keys={list(f.keys())} sub_count={len(sub)}")
        for sf in sub:
            er = sf.get('enum_ref')
            es = enums.get(er) if er else None
            ev_len = len(es['values']) if isinstance(es, dict) and 'values' in es else (len(es) if es else 0)
            print(f"      {sf.get('field')} ({sf.get('name')}): type={sf.get('type')} min={sf.get('min_value')} max={sf.get('max_value')} enum_ref={er}({ev_len}) target={sf.get('record_type') or sf.get('database_table_type') or sf.get('target')}")

# Also inspect db_tables_big.json for table numbers & counts
dbt = json.loads((ROOT / 'evidence/fm24/reports/dbdat_decode/db_tables_big.json').read_bytes())
print('\n=== 2. DB_TABLES_BIG KEYS & RELEVANT TABLES ===')
print('  top keys:', list(dbt.keys()))
for k, v in dbt.items():
    if isinstance(v, list):
        print(f'  list {k}: len={len(v)}')
        for item in v[:3]:
            print('    sample:', str(item)[:150])
    elif isinstance(v, dict) and k in ('tables', 'server', 'client'):
        print(f'  dict {k}: len={len(v)}')

# --- 2. PE static check: STARTING_RECORD table & global xrefs for +0x123, +0xda, base+0xac ---
PE_BYTES = EXE.read_bytes()
pe = pefile.PE(data=PE_BYTES, fast_load=True)
IB = pe.OPTIONAL_HEADER.ImageBase
va = lambda fo: IB + pe.get_rva_from_offset(fo)
fo_from_va = lambda v: pe.get_offset_from_rva(v - IB)
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

print('\n=== 3. STARTING_RECORD (TC_RECORD_GET @ 0x3ebad50) GLOBAL TABLE CHECK ===')
for ins in md.disasm(PE_BYTES[0x3ebad50:0x3ebae30], va(0x3ebad50)):
    fo = fo_from_va(ins.address)
    note = ''
    if 'rip' in ins.op_str:
        # compute target VA
        import re
        m = re.search(r'rip ([+-]) 0x([0-9a-f]+)', ins.op_str)
        if m:
            sign = 1 if m.group(1) == '+' else -1
            tva = ins.address + ins.size + sign * int(m.group(2), 16)
            try:
                note = f' ; target VA=0x{tva:x} (fo=0x{fo_from_va(tva):x})'
            except Exception:
                note = f' ; target VA=0x{tva:x}'
    print(f'  0x{fo:x}: {ins.mnemonic:8s} {ins.op_str}{note}')

# Find which DATABASE table registration in 0xf025c0..0xf04800 uses STARTING_RECORD RTTI!
sr_rtti_bytes = b'.?AV?$DATABASE_TABLE@VSTARTING_RECORD@db@@@db@@'
pos = PE_BYTES.find(sr_rtti_bytes)
print(f'  DATABASE_TABLE<STARTING_RECORD> RTTI at fo=0x{pos:x} (VA=0x{va(pos):x})' if pos != -1 else '  DATABASE_TABLE<STARTING_RECORD> RTTI not found')
# Search for all RTTI containing STARTING_RECORD
p0 = 0
while True:
    idx = PE_BYTES.find(b'STARTING_RECORD', p0)
    if idx == -1: break
    s = PE_BYTES[idx-25:idx+55]
    print(f'    RTTI/str @ 0x{idx:x}: {s!r}')
    p0 = idx + 15

# Find DATABASE_TABLE<STARTING_RECORD> vtable/COL/init!
if pos != -1:
    # TypeDescriptor starts 16 bytes before name string
    td_rva = pe.get_rva_from_offset(pos - 16)
    col_needle = struct.pack('<I', td_rva)
    p0 = 0
    while True:
        idx = PE_BYTES.find(col_needle, p0)
        if idx == -1: break
        # COL has signature=1 at idx-12
        if idx >= 12 and struct.unpack_from('<I', PE_BYTES, idx-12)[0] == 1:
            col_va = va(idx - 12)
            col_ptr = PE_BYTES.find(struct.pack('<Q', col_va))
            if col_ptr != -1:
                vt_fo = col_ptr + 8
                vt_va = va(vt_fo)
                print(f'  COL @ 0x{idx-12:x} -> vtable @ 0x{vt_fo:x} (VA=0x{vt_va:x})')
                # Search for lea reg, [rip + ...] pointing to vt_va in 0xf02000..0xf06000
                for ins in md.disasm(PE_BYTES[0xf02000:0xf06000], va(0xf02000)):
                    if ins.mnemonic == 'lea' and 'rip' in ins.op_str:
                        import re
                        m = re.search(r'rip ([+-]) 0x([0-9a-f]+)', ins.op_str)
                        if m:
                            sign = 1 if m.group(1) == '+' else -1
                            tva = ins.address + ins.size + sign * int(m.group(2), 16)
                            if tva == vt_va:
                                fo_hit = fo_from_va(ins.address)
                                print(f'  INIT HIT @ 0x{fo_hit:x}: {ins.mnemonic} {ins.op_str}')
                                for ins2 in md.disasm(PE_BYTES[fo_hit-0x30:fo_hit+0x140], va(fo_hit-0x30)):
                                    fo2 = fo_from_va(ins2.address)
                                    print(f'    0x{fo2:x}: {ins2.mnemonic:8s} {ins2.op_str}')
        p0 = idx + 4

# --- 3. Extract FMF members & full-archive vectorized item validation ---
def open_fmf(side):
    b = (DATA / f'{side}_db.dat').read_bytes()
    toc, base = (x + 17 for x in struct.unpack_from('<QQ', b, 17))
    assert base == 34 and b[8:17] == b[toc:toc+9] == b'\x02\x01fmf.\x08\x00\x00'
    def frame(buf):
        d = zstd.ZstdDecompressor().decompressobj()
        v = d.decompress(buf)
        return v, len(buf) - len(d.unused_data)
    directory, used = frame(b[toc+9:])
    assert toc + 9 + used == len(b)
    p = 0; entries = {}
    def pull(n):
        nonlocal p; r = directory[p:p+n]; p += n; return r
    def num(): return struct.unpack('<I', pull(4))[0]
    def text(): return pull(num()).decode('utf-8')
    def node(parent):
        prefix = parent + text() + '/'
        for _ in range(num()):
            name = prefix + text() + text()
            off, size, unpacked, _, _ = struct.unpack('<5Q', pull(40))
            entries[name] = (base + off, base + off + size, unpacked)
        for _ in range(num()): node(prefix)
    node('')
    def get(rel):
        lo, hi, n = entries[rel]
        q = lo; out = None
        while q < hi:
            pl, w = frame(b[q:hi]); q += w
            if len(pl) == n: out = pl
        assert out is not None and out[:8] == HEAD
        return out
    return entries, get

srv_ent, srv_get = open_fmf('server')
cli_ent, cli_get = open_fmf('client')
print('\n=== 4. FMF TABLE COUNTS FOR JOIN TARGETS ===')
join_counts = {}
for tnum in [3, 25, 29, 26, 21, 9, 2, 7, 13, 14, 15, 16, 17, 18, 19, 20, 35, 36, 37, 38, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69]:
    rel = f'server_db/table_{tnum}.dat'
    if rel in srv_ent:
        buf = srv_get(rel)
        cnt = struct.unpack_from('<I', buf, 8)[0]
        join_counts[tnum] = cnt
print('  key table counts:', {k: join_counts[k] for k in [2, 3, 7, 9, 21, 25, 29, 43, 59, 62, 66] if k in join_counts})
# Check people_db.dat or basic_people_db.dat or people tables in server_db!
print('  non-table server_db entries:', [k for k in sorted(srv_ent) if not k.startswith('server_db/table_')])
# Check people_db.dat if present in DATA
print('  DATA dir files:', sorted(p.name for p in DATA.iterdir()))

# Load table_3.dat UIDs (for club ordinal -> UID mapping & wrong-UID negative control)
# Wait: check t71 or extract table_3 ordinal->UID cleanly via server table_3? Wait: table_3 has variable length!
# Let's check scratch/t71/out/rows_extra3.json or client table_3 (or fixed stride?) - wait table_3 client/server is variable length,
# let's check if scratch/t63 or t57 has club ordinal->UID table, or check people count!
# Actually we can read server table_3 UIDs or check scratch/t71! Let's check what's in table_25 (comp) and table_29 (stage_name) and people_db.dat!
for pfile in ['people_db.dat', 'server_db.dat']:
    fp = DATA / pfile
    if fp.exists() and pfile == 'people_db.dat':
        b = fp.read_bytes()
        print(f'  people_db.dat size={len(b)}')

# Parse ALL items of ALL 16 list fields + election + Cown + extra+0xa0[0..5] in server_db/table_extra_3.dat!
srv_ex3 = srv_get('server_db/table_extra_3.dat')
cli_ex3 = cli_get('client_db/table_extra_3.dat')
N = struct.unpack_from('<I', srv_ex3, 8)[0]
assert N == 84259

# Collect detailed item records
cscm_items = []    # (row, raw22)
cpsl_items = []    # (row, tag, raw10)
cspb_items = []    # (row, raw20)
cren_items = []    # (row, raw6)
tcrs_items = []    # (row, iv, raw10)
kit_items = []     # (row, tag, raw26)
vtag_items = defaultdict(list)  # tag -> list of (row, bytes)
elec_rows = []     # (row, club_ord, d1, d2, bitmask, b12, b13, b14, b15, b16)
cown_arr = np.empty(N, dtype=np.int8)
a0_dates = np.empty((N, 6), dtype='<u4')
uf_rows = {}       # row -> list of 10 i32
ctlv_arr = np.empty(N, dtype=np.int8)
catd_arr = np.empty(N, dtype='<i4')
tcht_map = {}

p = 12
for row in range(N):
    ord_ = struct.unpack_from('<I', srv_ex3, p)[0]; p += 4
    assert ord_ == row
    c18 = struct.unpack_from('<H', srv_ex3, p)[0]; p += 2
    assert c18 == 0
    # +0x80(4), +0x84(4), +0x88[6](24), flag_a0(1)=1, +0xa0[6](24), +0xb8(4), +0xbc(4), +0x120..12f(16)
    p += 4 + 4 + 24
    fa0 = srv_ex3[p]; p += 1
    assert fa0 == 1
    a0_dates[row] = struct.unpack_from('<6I', srv_ex3, p); p += 24
    p += 4 + 4
    # 16 bytes: +120..+12f (note: exact order in 0xe5d210!)
    # wait verify order of +120..+12f! In recon11:
    # b0=+120(Ctlv), b1=+121(Cmle), b2=+122, b3=+123, b4=+125, b5=+126(Cyim), b6=+127(CScP),
    # b7=+128, b8=+129(Cown), b9=+12a(Chti), b10=+12b(Cyfb), b11=+12c(Cytv), b12=+12d(Crcb), b13=+12e, b14=+12f
    # Wait that's 15 bytes! Let's check exact byte offset of elec flag = r+83!
    # 4(ord)+2(c18)+4(80)+4(84)+24(88)+1(fa0)+24(a0)+4(b8)+4(bc) = 71!
    # Wait 83 - 71 = 12? Let's check recon11 exact offsets!
    break

print('\nChecking exact recon11 server parser offsets (lines 110..260)...')
with open(ROOT / 'scratch/t82/recon11_profile_all.py', 'r', encoding='utf-8') as f:
    r11_lines = f.read().splitlines()
for idx, ln in enumerate(r11_lines[105:270], 106):
    print(f'  {idx:3d}: {ln}')
