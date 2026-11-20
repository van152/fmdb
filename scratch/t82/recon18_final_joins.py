"""Final check of table_25/table_23/table_3 joins + Cspb/Cren/TCrs exact layouts + Tko1..3 schema & setters."""
import json, os, struct, sys
from collections import Counter
from pathlib import Path
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import zstandard as zstd
import pefile, capstone

ROOT = Path(r'D:\tmp2b\fm24-db')
DATA = Path(os.environ.get('FM24_DB_DIR', ROOT / 'scratch/data'))
EXE = Path(r'D:\tmp2b\fm24\input\editor.exe')
HEAD = bytes.fromhex('03017461642ef10d')

def open_fmf(side):
    b = (DATA / f'{side}_db.dat').read_bytes()
    toc, base = (x + 17 for x in struct.unpack_from('<QQ', b, 17))
    def frame(buf):
        d = zstd.ZstdDecompressor().decompressobj()
        v = d.decompress(buf)
        return v, len(buf) - len(d.unused_data)
    directory, _ = frame(b[toc+9:])
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

# 1. Extract ALL comp UIDs from client_db/table_25.dat (known stride 126 from t59/t64: 14+7047*126+... wait check!)
t25 = cli_get('client_db/table_25.dat')
cnt25 = struct.unpack_from('<I', t25, 8)[0]
comp_uids = set()
# Remember table_25 client rows have selector 1B + body + 12B identity; check exact stride via (len-22)/cnt or variable!
print(f'table_25 cli: len={len(t25)} cnt={cnt25} (len-22)/cnt={(len(t25)-22)/cnt25:.4f}')
# Check table_25 by scanning ordinal 0,1,2,3 in first 1000 bytes!
for st in range(100, 140):
    for start in range(12, 160):
        if start + 4*st + 12 <= len(t25):
            vals = [struct.unpack_from('<I', t25, start + k*st)[0] for k in range(5)]
            if vals == [0, 1, 2, 3, 4]:
                u0a, u0b = struct.unpack_from('<II', t25, start + 4)
                u1a, u1b = struct.unpack_from('<II', t25, start + st + 4)
                if u0a == u0b and u1a == u1b:
                    print(f'  t25 stride={st} first_id={start}: row0=({vals[0]},{u0a}) row1=({vals[1]},{u1a})')
                    # Wait: table_25 has variable rows (strings?) or fixed? Let's test if all 7047 match fixed stride!
                    ok = sum(1 for k in range(cnt25) if start + k*st + 12 <= len(t25) and struct.unpack_from('<I', t25, start + k*st)[0] == k)
                    print(f'    fixed-stride match: {ok}/{cnt25}')

# Check client_db/table_23.dat & server_db/table_23.dat (STAGE_NAME)!
t23_uids = set()
for side_nm, ent, get in [('client', cli_ent, cli_get), ('server', srv_ent, srv_get)]:
    rel = f'{side_nm}_db/table_23.dat'
    if rel in ent:
        t23 = get(rel)
        cnt23 = struct.unpack_from('<I', t23, 8)[0]
        print(f'{rel}: len={len(t23)} cnt={cnt23} (len-22)/cnt={(len(t23)-22)/cnt23:.4f} first48={t23[:48].hex()}')
        if (len(t23) - 22) % cnt23 == 0:
            st = (len(t23) - 22) // cnt23
            for off in range(st - 11):
                if [struct.unpack_from('<I', t23, 13 + k*st + off)[0] for k in range(5)] == [0, 1, 2, 3, 4]:
                    print(f'  t23 FIXED stride={st} off={off}: row0={struct.unpack_from("<III", t23, 13+off)} row1={struct.unpack_from("<III", t23, 13+st+off)}')
                    for k in range(cnt23):
                        o, u1, u2 = struct.unpack_from('<III', t23, 13 + k*st + off)
                        assert o == k and u1 == u2
                        t23_uids.add(u1)

# Extract comp UIDs from db_tables_big or table_25? Wait check how table_25 is structured or check scratch/t59/t64!
# Even simpler: check scratch/t71/out/rows_extra3.json or client table_3 UIDs!
# Wait: let's check client_db/table_25.dat first 300 bytes to see why fixed stride didn't match all 7047 (it's almost fixed: 127.003B - only a few rows have inline strings!)
# Wait: for table_25, let's find ALL triples (ord, u1, u2) with ord=0..7046 & u1==u2 sequentially!
pos = 12
for k in range(cnt25):
    needle = struct.pack('<I', k)
    found = False
    search_start = pos
    while True:
        idx = t25.find(needle, search_start, min(len(t25), pos + 400))
        if idx == -1: break
        if idx + 12 <= len(t25):
            u1, u2 = struct.unpack_from('<II', t25, idx + 4)
            if u1 == u2 and 1 <= u1 <= 2100000000:
                comp_uids.add(u1)
                pos = idx + 12
                found = True
                break
        search_start = idx + 1
    if not found:
        print(f'  t25 seq scan stopped at k={k} pos={pos}')
        break
print(f'  table_25 extracted UIDs: {len(comp_uids)} / {cnt25}, end_pos={pos}/{len(t25)}')

# Same for table_3 club UIDs!
t3 = cli_get('client_db/table_3.dat')
cnt3 = struct.unpack_from('<I', t3, 8)[0]
club_uids = set()
club_ord_to_uid = {}
pos = 12
for k in range(cnt3):
    needle = struct.pack('<I', k)
    found = False
    search_start = pos
    while True:
        idx = t3.find(needle, search_start, min(len(t3), pos + 400))
        if idx == -1: break
        if idx + 12 <= len(t3):
            u1, u2 = struct.unpack_from('<II', t3, idx + 4)
            if u1 == u2 and 1 <= u1 <= 2100000000:
                club_uids.add(u1); club_ord_to_uid[k] = u1
                pos = idx + 12
                found = True
                break
        search_start = idx + 1
    if not found:
        print(f'  t3 seq scan stopped at k={k} pos={pos}')
        break
print(f'  table_3 extracted UIDs: {len(club_uids)} / {cnt3}, end_pos={pos}/{len(t3)}, ord460->UID={club_ord_to_uid.get(460)}, ord1297->UID={club_ord_to_uid.get(1297)}, ord623->UID={club_ord_to_uid.get(623)}, ord463->UID={club_ord_to_uid.get(463)}')

# Check Tko1..3 / Tkg1..3 schema + TC_EXTRA_SET disasm + TCrs item reader 0x155cb20 -> thunk!
master = json.loads((ROOT / 'evidence/fm24/reports/editor_schema/master.json').read_bytes())
for i, f in enumerate(master['entities']['club.xml'][0]['fields']):
    if f['field'] in ('Tko1', 'Tkg1', 'Tko2', 'Tkg2', 'Tko3', 'Tkg3'):
        print(f'  club.xml[{i}] {f["field"]}: type={f["type"]} name={f["name"]}')
ftjn_vals = set(int(v['enum']) for v in master['enums']['ftjn']['values'])

# Disasm TCrs item reader helper 0x155c120 (0x14155cb20 -> fo 0x155c120)
PE = EXE.read_bytes()
pe = pefile.PE(data=PE, fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase
va = lambda fo: IB + pe.get_rva_from_offset(fo)
fo_va = lambda v: pe.get_offset_from_rva(v - IB)
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)
tfo = fo_va(0x14155cb20)
if PE[tfo] == 0xe9:
    tfo = fo_va(0x14155cb20 + 5 + struct.unpack_from('<i', PE, tfo+1)[0])
print(f'\n=== TCRS_SUB_RDR @ 0x{tfo:x} ===')
sva = va(tfo)
for ins in md.disasm(PE[tfo:tfo+0x220], sva):
    cfo = ins.address - sva + tfo
    print(f'  0x{cfo:x}: {ins.mnemonic:8s} {ins.op_str}')
    if ins.mnemonic == 'ret' and PE[cfo+ins.size] in (0xcc, 0x90): break

# Full exact replay of Cscm, Cspb, Cren, TCrs, Csoc, Camc, Cbbl with real UID/ordinal joins!
srv_ex3 = srv_get('server_db/table_extra_3.dat')
N = struct.unpack_from('<I', srv_ex3, 8)[0]

def date4_ok(u):
    yr = (u >> 16) & 0xffff; doy = u & 0x1ff; mid = (u >> 9) & 0x7f
    leap = 1 if (yr % 4 == 0 and (yr % 100 != 0 or yr % 400 == 0)) else 0
    return (yr >= 1) and (1 <= doy <= 365 + leap) and (mid == 0)

cscm = []; cspb = []; cren = []; tcrs = []; csoc = []; camc = []; cbbl = []
p = 12
for i in range(N):
    p += 7
    c18 = struct.unpack_from('<H', srv_ex3, p)[0]; p += 2 + 4 * c18
    p += 34
    ef = srv_ex3[p]; p += 1 + (24 if ef else 0)
    p += 15
    elf = srv_ex3[p]; p += 1 + (19 if elf else 0)
    p += 5 + 21 + 21
    ta = srv_ex3[p]; p += 1 + (7 if ta > 1 else 6)
    tb = srv_ex3[p]; p += 1 + (12 if tb < 2 else 14 if tb == 2 else 15)
    p += 25
    c28 = struct.unpack_from('<b', srv_ex3, p)[0]; p += 1
    for _ in range(c28):
        ver, co1, co2, stnm, sn1, sn2, tl = struct.unpack_from('<Biibiii', srv_ex3, p)
        cscm.append((i, co1, co2, stnm, sn1, sn2)); p += 22
    c20 = srv_ex3[p]; p += 1 + 10 * c20
    f48 = srv_ex3[p]; p += 1
    if f48:
        t48 = struct.unpack_from('<b', srv_ex3, p)[0]; p += 1
        p += (24 if t48 > 0 else 16)
        cnt48 = srv_ex3[p]; p += 1 + 4 * cnt48
    p += 7
    c68 = struct.unpack_from('<H', srv_ex3, p)[0]; p += 2 + 11 * c68
    p += 3 + 8
    tlen = struct.unpack_from('<I', srv_ex3, p)[0]; p += 4 + tlen
    kcnt = srv_ex3[p]; p += 1 + 27 * kcnt
    p += 8
    c18b = struct.unpack_from('<h', srv_ex3, p)[0]; p += 2
    for _ in range(c18b):
        # 0x3ea5150: 1B ver, 8B cmid(u1,u2), 1B venu(+0), 1B matc(+1), 1B type(+2), 4B stdt(+c), 4B endt(+10)
        ver, cm1, cm2, venu, matc, btype, stdt, endt = struct.unpack_from('<BiibbbII', srv_ex3, p)
        cspb.append((i, ver, cm1, cm2, venu, matc, btype, stdt, endt)); p += 20
    c30b = struct.unpack_from('<b', srv_ex3, p)[0]; p += 1
    for _ in range(c30b):
        # 0x11d4590: 1B rsnn(+8), 4B rsnp(+0), 1B rsnr(+9)
        rsnn, rsnp, rsnr = struct.unpack_from('<bib', srv_ex3, p)
        cren.append((i, rsnn, rsnp, rsnr)); p += 6
    p += 16
    cb0 = struct.unpack_from('<H', srv_ex3, p)[0]; p += 2
    for _ in range(cb0):
        t = srv_ex3[p]; p += 1
        if t == 5:
            p1, p2, club_ord, perc = struct.unpack_from('<iiib', srv_ex3, p)
            csoc.append((i, p1, club_ord, perc)); p += 24
        elif t == 6:
            p1, p2, club_ord, cash, apps, apfr, ctype = struct.unpack_from('<iiiibbb', srv_ex3, p)
            camc.append((i, p1, club_ord, cash, apps, apfr, ctype)); p += 19
        elif t == 7:
            p1, p2, cash, club_ord = struct.unpack_from('<iiii', srv_ex3, p)
            cbbl.append((i, p1, cash, club_ord)); p += 24
        elif t == 4: p += 43
        elif t == 37: p += 27
        elif t == 9:
            p += 20
            for _ in range(4):
                sl = struct.unpack_from('<I', srv_ex3, p)[0]; p += 4 + sl
        elif t == 16:
            c16 = struct.unpack_from('<b', srv_ex3, p)[0]; p += 1 + 4 * c16
        elif t == 38:
            c38 = struct.unpack_from('<I', srv_ex3, p)[0]; p += 4
            for _ in range(c38):
                p += 19; sl = struct.unpack_from('<I', srv_ex3, p)[0]; p += 4 + sl
    f48b = srv_ex3[p]; p += 1
    if f48b:
        v48, c48 = struct.unpack_from('<II', srv_ex3, p); p += 8
        for _ in range(c48):
            iv = struct.unpack_from('<h', srv_ex3, p)[0]; p += 2
            sz = 8 + (iv >= 2) + (iv >= 3)
            tcrs.append((i, iv, srv_ex3[p:p+sz])); p += sz
assert p == len(srv_ex3)

print('\n=== VERIFIED JOIN & DOMAIN RESULTS ===')
# Cscm
cscm_co_miss = [x for x in cscm if x[1] != -1 and x[1] not in comp_uids]
cscm_sn_zero = [x for x in cscm if x[4] == 0]
cscm_sn_miss = [x for x in cscm if x[4] not in (-1, 0) and x[4] not in t23_uids]
print(f'[Cscm] {len(cscm)} items:')
print(f'  stco in table_25 UIDs: miss={len(cscm_co_miss)} (sample={cscm_co_miss[:3]})')
print(f'  slsn: zero={len(cscm_sn_zero)}, null(-1)={sum(x[4]==-1 for x in cscm)}, non-zero miss vs table_23 UIDs={len(cscm_sn_miss)} (distinct slsn={Counter(x[4] for x in cscm)})')

# Cspb
cspb_co_miss = [x for x in cspb if x[2] != -1 and x[2] not in comp_uids]
print(f'\n[Cspb] {len(cspb)} items across {len(set(x[0] for x in cspb))} rows:')
print(f'  ver={Counter(x[1] for x in cspb)}, cmid eq={sum(x[2]==x[3] for x in cspb)}/{len(cspb)}, null={sum(x[2]==-1 for x in cspb)}, miss_t25={len(cspb_co_miss)}')
print(f'  venu={dict(sorted(Counter(x[4] for x in cspb).items()))}')
print(f'  matc={dict(sorted(Counter(x[5] for x in cspb).items()))} (note: getter suppresses -1!)')
print(f'  type={dict(sorted(Counter(x[6] for x in cspb).items()))}')
print(f'  stdt_bad={sum(not date4_ok(x[7]) for x in cspb)}, endt_bad={sum(not date4_ok(x[8]) for x in cspb)}')

# Cren
cren_n_bad = [x for x in cren if not (1 <= x[1] <= 99)]
print(f'\n[Cren] {len(cren)} items across {len(set(x[0] for x in cren))} rows:')
print(f'  rsnn: min={min(x[1] for x in cren)} max={max(x[1] for x in cren)} viol_1_99={len(cren_n_bad)} first={cren_n_bad[:3]}')
print(f'  rsnp: min={min(x[2] for x in cren)} max={max(x[2] for x in cren)} null(-1)={sum(x[2]==-1 for x in cren)} neg_other={sum(x[2]<-1 for x in cren)} sample={[x[2] for x in cren if x[2]!=-1][:8]}')
print(f'  rsnr: {dict(sorted(Counter(x[3] for x in cren).items()))}')

# Wrong-UID negative control for Csoc.club, Camc.club, Cbbl.club (all are ordinals 0..84258, NOT club UIDs!)
for nm, arr, idx_c in [('Csoc.club', csoc, 2), ('Camc.club', camc, 2), ('Cbbl.club', cbbl, 3)]:
    in_ord = sum(0 <= x[idx_c] < 84259 for x in arr)
    in_uid = sum(x[idx_c] in club_uids for x in arr)
    print(f'[{nm}] total={len(arr)} valid_ordinal={in_ord}/{len(arr)} wrong_UID_hits={in_uid}/{len(arr)} (wrong_UID_miss={len(arr)-in_uid})')
