"""Comprehensive item-level validation of ALL 16 list fields + reader wire-offset check +
election/Cown invariants + extra+0xa0 dates + known-club L2 anchors."""
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

PE = EXE.read_bytes()
pe = pefile.PE(data=PE, fast_load=True)
IB = pe.OPTIONAL_HEADER.ImageBase
va = lambda fo: IB + pe.get_rva_from_offset(fo)
fo_va = lambda v: pe.get_offset_from_rva(v - IB)
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

def dump_fn(name, fo, sz=0x280):
    print(f'\n=== DISASM {name} @ 0x{fo:x} (VA 0x{va(fo):x}) ===')
    sva = va(fo)
    for ins in md.disasm(PE[fo:fo+sz], sva):
        cfo = ins.address - sva + fo
        extra = ''
        if ins.mnemonic in ('call', 'jmp') and ins.op_str.startswith('0x'):
            try:
                tva = int(ins.op_str, 16); tfo = fo_va(tva)
                extra = f' ; -> 0x{tfo:x}'
                if PE[tfo] == 0xe9:
                    rel = struct.unpack_from('<i', PE, tfo+1)[0]
                    extra += f' (thunk->0x{fo_va(tva+5+rel):x})'
            except Exception:
                pass
        print(f'  0x{cfo:x}: {ins.mnemonic:8s} {ins.op_str}{extra}')
        if ins.mnemonic == 'ret' and PE[cfo+ins.size] in (0xcc, 0x90):
            break

# 1. Disassemble the 4 polymorphic item readers + TCrs item reader + Cspb/Cren/Cscm/CPsL reader snippets
for nm, foff, sz in [
    ('VTAG5_RDR_NEXT_SALE', 0x42d2710, 0x220),
    ('VTAG6_RDR_APP_MONEY', 0x42d6a10, 0x220),
    ('VTAG7_RDR_BUY_BACK', 0x42c66f0, 0x260),
    ('VTAG38_RDR_TESTIMONIAL', 0x14da470, 0x280),
    ('TCRS_ITEM_RDR_CHECK', 0x11d3850, 0x200),
]:
    dump_fn(nm, foff, sz)

# 2. Extract FMF members
def open_fmf(side):
    b = (DATA / f'{side}_db.dat').read_bytes()
    toc, base = (x + 17 for x in struct.unpack_from('<QQ', b, 17))
    def frame(buf):
        d = zstd.ZstdDecompressor().decompressobj()
        v = d.decompress(buf)
        return v, len(buf) - len(d.unused_data)
    directory, used = frame(b[toc+9:])
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
srv_ex3 = srv_get('server_db/table_extra_3.dat')
cli_ex3 = cli_get('client_db/table_extra_3.dat')
N = struct.unpack_from('<I', srv_ex3, 8)[0]
assert N == 84259

def list_fmf(raw):
    toc, base = (x + 17 for x in struct.unpack_from('<QQ', raw, 17))
    d = zstd.ZstdDecompressor().decompressobj()
    directory = d.decompress(raw[toc+9:])
    p = 0; ents = {}
    def pull(n):
        nonlocal p; r = directory[p:p+n]; p += n; return r
    def num(): return struct.unpack('<I', pull(4))[0]
    def text(): return pull(num()).decode('utf-8')
    def node(parent):
        prefix = parent + text() + '/'
        for _ in range(num()):
            name = prefix + text() + text()
            off, size, unpacked, _, _ = struct.unpack('<5Q', pull(40))
            ents[name] = (base + off, base + off + size, unpacked)
        for _ in range(num()): node(prefix)
    node('')
    return ents

print('\n=== PEOPLE DB & TABLE 45 CHECK ===')
if 'server_db/table_45.dat' in srv_ent:
    t45 = srv_get('server_db/table_45.dat')
    print(f'  server_db/table_45.dat (STARTING_RECORD): {len(t45)}B cnt={struct.unpack_from("<I", t45, 8)[0]}')
for pname in ['people_db.dat', 'basic_people_db.dat']:
    fp = DATA / pname
    raw = fp.read_bytes()
    if raw[:8] == HEAD:
        print(f'  {pname}: direct tad., count={struct.unpack_from("<I", raw, 8)[0]}')
    elif raw[8:14] == b'\x02\x01fmf.':
        ents = list_fmf(raw)
        print(f'  {pname}: FMF with {len(ents)} members: {list(ents.keys())[:10]}')
    else:
        print(f'  {pname}: magic={raw[:20].hex()}')

# Load club UIDs from table_3? Wait: check how t71 gets club ordinal -> UID!
# Let's check server_db/table_3.dat via t71 or extract club UIDs directly?
# Actually in client_db/table_3.dat we know rows_extra3.json or client_db/table_3.dat layout! Let's check!
t3_cli = cli_get('client_db/table_3.dat')
t25_cli = cli_get('client_db/table_25.dat')
t29_srv = srv_get('server_db/table_29.dat')
print(f'  table_3 cli: {len(t3_cli)}B cnt={struct.unpack_from("<I", t3_cli, 8)[0]}')
print(f'  table_25 cli: {len(t25_cli)}B cnt={struct.unpack_from("<I", t25_cli, 8)[0]}')
print(f'  table_29 srv: {len(t29_srv)}B cnt={struct.unpack_from("<I", t29_srv, 8)[0]}')

# Check master.json enums['ftjn']
master = json.loads((ROOT / 'evidence/fm24/reports/editor_schema/master.json').read_bytes())
ftjn_vals = set(int(v['enum']) for v in master['enums']['ftjn']['values'])
print(f'  enums[ftjn] ({len(ftjn_vals)} vals): {sorted(ftjn_vals)}')

# Full replay collecting EVERY item of EVERY list + invariants!
def date4_ok(u):
    yr = (u >> 16) & 0xffff
    doy = u & 0x1ff
    mid = (u >> 9) & 0x7f
    leap = 1 if (yr % 4 == 0 and (yr % 100 != 0 or yr % 400 == 0)) else 0
    return (yr >= 1) and (1 <= doy <= 365 + leap) and (mid == 0), (u == 0x076c0001)

cscm_items = []
cpsl_items = []
cspb_items = []
cren_items = []
tcrs_items = []
kit_rows = []
vtag = defaultdict(list)

elec_flag = np.zeros(N, dtype=np.uint8)
elec_club = np.full(N, -1, dtype=np.int32)
cown = np.zeros(N, dtype=np.int8)
ea0_dates = np.zeros((N, 6), dtype=np.uint32)
cuf_map = {}
ctlv = np.zeros(N, dtype=np.int8)
cyfb = np.zeros(N, dtype=np.int8)
cytv = np.zeros(N, dtype=np.int8)
crcb = np.zeros(N, dtype=np.int8)
cmle = np.zeros(N, dtype=np.int8)
cyim = np.zeros(N, dtype=np.int8)
catd = np.zeros(N, dtype=np.int32)
cmna = np.zeros(N, dtype=np.int32)
cmxa = np.zeros(N, dtype=np.int32)
csly = np.zeros(N, dtype=np.int8)
cyfn = np.zeros(N, dtype=np.uint16)
tcht = {}
kit_by_bucket = Counter()
kit_row_buckets = defaultdict(set)

p = 12
for i in range(N):
    o = struct.unpack_from('<I', srv_ex3, p)[0]; p += 4
    assert o == i
    ctlv[i], cmle[i], _ = struct.unpack_from('<bbb', srv_ex3, p); p += 3
    c18 = struct.unpack_from('<H', srv_ex3, p)[0]; p += 2; p += 4 * c18
    p += 5 + 1 + 4 + 24 # da, 123, c0, 88[6]
    ef = srv_ex3[p]; p += 1
    if ef:
        ea0_dates[i] = struct.unpack_from('<6I', srv_ex3, p); p += 24
    p += 15 # de, b8, 125, 84, 80
    elf = srv_ex3[p]; p += 1
    elec_flag[i] = elf
    if elf:
        elec_club[i] = struct.unpack_from('<i', srv_ex3, p)[0]
        p += 19
    cyim[i], _cscp, _128, cown[i], _chti = struct.unpack_from('<5b', srv_ex3, p); p += 5
    p += 1 # f8_ver
    csly[i] = struct.unpack_from('<b', srv_ex3, p + 8)[0]
    p += 20
    p += 1 + 20 # p10c
    ta = srv_ex3[p]; p += 1 + (7 if ta > 1 else 6)
    tb = srv_ex3[p]; p += 1 + (12 if tb < 2 else 14 if tb == 2 else 15)
    _, _, _, cyfb[i], cytv[i], crcb[i], _, _, _, _ = struct.unpack_from('<Iiibbbbbii', srv_ex3, p); p += 25
    # +28 (Cscm)
    c28 = struct.unpack_from('<b', srv_ex3, p)[0]; p += 1
    for _ in range(c28):
        cscm_items.append((i, srv_ex3[p:p+22])); p += 22
    # +20
    c20 = srv_ex3[p]; p += 1; p += 10 * c20
    # +48 (UEFA coeff)
    f48 = srv_ex3[p]; p += 1
    if f48:
        t48 = struct.unpack_from('<b', srv_ex3, p)[0]; p += 1
        p += (24 if t48 > 0 else 16)
        cnt48 = srv_ex3[p]; p += 1
        vals48 = list(struct.unpack_from(f'<{cnt48}i', srv_ex3, p))
        p += 4 * cnt48
        cuf_map[i] = [round(v / 1000.0, 3) for v in vals48]
    p += 7 # +30/+38/+70/+50 all 0
    # +68 (CPsL)
    c68 = struct.unpack_from('<H', srv_ex3, p)[0]; p += 2
    for _ in range(c68):
        cpsl_items.append((i, srv_ex3[p], srv_ex3[p+1:p+11])); p += 11
    p += 1 + 2 # +40 + dc
    # Common tail
    cyfn[i] = struct.unpack_from('<H', srv_ex3, p)[0]
    p += 8 # d8, cc, base_ac
    tlen = struct.unpack_from('<I', srv_ex3, p)[0]; p += 4
    if tlen:
        tcht[i] = srv_ex3[p:p+tlen].decode('utf-8')
        p += tlen
    kcnt = srv_ex3[p]; p += 1
    for _ in range(kcnt):
        ot = srv_ex3[p]; p += 1
        # +18(4B), +1c(4B), +20(2B yr), +22(1B kit_type), +23, +24, +25(outfield)
        c18k, c1ck, kyr, b22, b23, b24, b25 = struct.unpack_from('<iiHBBBB', srv_ex3, p+12)
        kit_by_bucket[(b22, 1 if b25 else 0)] += 1
        kit_row_buckets[(b22, 1 if b25 else 0)].add(i)
        p += 26
    p += 8 # base_a0, base_a8
    # Server tail
    c18b = struct.unpack_from('<h', srv_ex3, p)[0]; p += 2
    for _ in range(c18b):
        cspb_items.append((i, srv_ex3[p:p+20])); p += 20
    c30b = struct.unpack_from('<b', srv_ex3, p)[0]; p += 1
    for _ in range(c30b):
        cren_items.append((i, srv_ex3[p:p+6])); p += 6
    _, _, _, _, catd[i], cmna[i], cmxa[i] = struct.unpack_from('<bbbbiii', srv_ex3, p); p += 16
    cb0 = struct.unpack_from('<H', srv_ex3, p)[0]; p += 2
    for _ in range(cb0):
        t = srv_ex3[p]; p += 1
        sp = p
        if t in (4, 5, 6, 7, 37):
            p += {4:43, 5:24, 6:19, 7:24, 37:27}[t]
        elif t == 9:
            p += 20
            for _ in range(4):
                sl = struct.unpack_from('<I', srv_ex3, p)[0]; p += 4 + sl
        elif t == 16:
            c16 = struct.unpack_from('<b', srv_ex3, p)[0]; p += 1 + 4 * c16
        elif t == 38:
            c38 = struct.unpack_from('<I', srv_ex3, p)[0]; p += 4
            for _ in range(c38):
                p += 1
                m38 = struct.unpack_from('<I', srv_ex3, p)[0]; p += 4 + 14
                sl = struct.unpack_from('<I', srv_ex3, p)[0]; p += 4 + sl
        if t in (4, 5, 6, 7, 16, 37, 38):
            vtag[t].append((i, srv_ex3[sp:p]))
    f48b = srv_ex3[p]; p += 1
    if f48b:
        v48, c48 = struct.unpack_from('<II', srv_ex3, p); p += 8
        for _ in range(c48):
            iv = struct.unpack_from('<h', srv_ex3, p)[0]; p += 2
            sz = 8 + (iv >= 2) + (iv >= 3)
            tcrs_items.append((i, iv, srv_ex3[p:p+sz])); p += sz
assert p == len(srv_ex3)

print('\n=== INVARIANTS CHECK ===')
el_idx = np.where(elec_flag == 1)[0]
print(f'  elec_flag==1 count: {len(el_idx)}')
print(f'  elec_club == row_ordinal on elec rows: {int(np.sum(elec_club[el_idx] == el_idx))} / {len(el_idx)}')
cown_in_37 = np.isin(cown, [3, 7])
print(f'  Cown in {{3,7}} count: {int(np.sum(cown_in_37))}, exact match with elec_flag==1: {int(np.sum((elec_flag==1) == cown_in_37))} / {N}')
print(f'  Cown histogram when elec_flag==1: {Counter(cown[el_idx].tolist())}')
print(f'  Cown histogram when elec_flag==0: {Counter(cown[elec_flag==0].tolist())}')
# ea0_dates
non_sent_ea0 = int(np.sum(ea0_dates != 0x076c0001))
print(f'  extra+0xa0[0..5] non-sentinel (not 1900-01-01): {non_sent_ea0} / {N*6}')
if non_sent_ea0:
    for col in range(6):
        ns = ea0_dates[:, col][ea0_dates[:, col] != 0x076c0001]
        if len(ns): print(f'    col {col}: {len(ns)} non-sentinel, sample={[hex(int(x)) for x in ns[:5]]}')

print('\n=== LIST ITEM DOMAIN VALIDATION ===')
# 1. Cscm (22B): inspect exact offsets from recon12: +0(8B comp), +8(1B stnm), +c(8B slsn)? Wait 22B wire -> let's unpack!
print(f'1. Cscm (+0x28): {len(cscm_items)} items across {len(set(r for r,_ in cscm_items))} rows')
cscm_stco0 = Counter(); cscm_stco1 = Counter(); cscm_stnm = Counter(); cscm_slsn0 = Counter(); cscm_slsn1 = Counter(); cscm_tail = Counter()
for r, raw in cscm_items:
    # print first 5 raw hex to verify exact layout
    pass
for r, raw in cscm_items[:5]:
    print(f'    sample row={r}: hex={raw.hex()}  <iibiii?={struct.unpack("<iibiiib", raw[:22]) if False else struct.unpack("<iibiiiB", raw[:22]) if False else None}')
    # wait 22 = 4+4+1+4+4+4+1 or 4+4+4+4+4+2! Let's unpack <ii b ii i ? no 4+4+1+4+4+4=21! Let's check <bb i i i i?
    print(f'      u32s={struct.unpack_from("<5i", raw, 0)} tail2={raw[20:22].hex()}')
    print(f'      alt: raw[0:8]={struct.unpack_from("<ii", raw, 0)} b8={struct.unpack_from("<b", raw, 8)[0]} raw[9:22]={raw[9:].hex()}')

# 2. CPsL (1B tag + 10B):
print(f'\n2. CPsL (+0x68): {len(cpsl_items)} items across {len(set(r for r,_,_ in cpsl_items))} rows')
cpsl_tags = Counter(tg for _, tg, _ in cpsl_items)
p1s = [struct.unpack_from('<i', raw, 0)[0] for _, _, raw in cpsl_items]
p2s = [struct.unpack_from('<i', raw, 4)[0] for _, _, raw in cpsl_items]
u8s = [struct.unpack_from('<H', raw, 8)[0] for _, _, raw in cpsl_items]
print(f'    tags={cpsl_tags}')
print(f'    per1: min={min(p1s)} max={max(p1s)} neg={sum(x<0 for x in p1s)} zero={sum(x==0 for x in p1s)} sample={p1s[:6]}')
print(f'    per2: min={min(p2s)} max={max(p2s)} neg={sum(x<0 for x in p2s)} zero={sum(x==0 for x in p2s)} sample={p2s[:6]}')
print(f'    +8 u16: {Counter(u8s).most_common(10)}')

# 3. Cspb (base+0x18, 20B):
print(f'\n3. Cspb (base+0x18): {len(cspb_items)} items across {len(set(r for r,_ in cspb_items))} rows')
for r, raw in cspb_items[:5]:
    print(f'    sample row={r}: hex={raw.hex()}  <bbbbiiII={struct.unpack("<bbbbiiII", raw)}')
v_venu = Counter(); v_matc = Counter(); v_type = Counter(); v_pad = Counter(); v_d1_bad = 0; v_d2_bad = 0; v_cm0 = []
for r, raw in cspb_items:
    venu, matc, btype, pad, cm0, cm1, d1, d2 = struct.unpack('<bbbbiiII', raw)
    v_venu[venu] += 1; v_matc[matc] += 1; v_type[btype] += 1; v_pad[pad] += 1; v_cm0.append((cm0, cm1))
    ok1, _ = date4_ok(d1); ok2, _ = date4_ok(d2)
    if not ok1: v_d1_bad += 1
    if not ok2: v_d2_bad += 1
print(f'    venu={dict(sorted(v_venu.items()))} matc={dict(sorted(v_matc.items()))} type={dict(sorted(v_type.items()))} pad={dict(v_pad)}')
print(f'    cmid_pairs[:6]={v_cm0[:6]} d1_bad={v_d1_bad} d2_bad={v_d2_bad}')

# 4. Cren (base+0x30, 6B):
print(f'\n4. Cren (base+0x30): {len(cren_items)} items across {len(set(r for r,_ in cren_items))} rows')
cr_p = []; cr_n = Counter(); cr_r = Counter(); bad_n = []
for r, raw in cren_items:
    po, num, rsn = struct.unpack('<ibb', raw)
    cr_p.append(po); cr_n[num] += 1; cr_r[rsn] += 1
    if not (1 <= num <= 99): bad_n.append((r, po, num, rsn))
print(f'    rsnp: min={min(cr_p)} max={max(cr_p)} neg={sum(x<0 for x in cr_p)} sample={cr_p[:8]}')
print(f'    rsnn: min={min(cr_n)} max={max(cr_n)} viol_1_99={len(bad_n)} first_viol={bad_n[:5]}')
print(f'    rsnr: {dict(sorted(cr_r.items()))}')

# 5. TCrs (base+0x48, iv=3 + 10B):
print(f'\n5. TCrs (base+0x48): {len(tcrs_items)} items across {len(set(r for r,_,_ in tcrs_items))} rows')
for r, iv, raw in tcrs_items[:5]:
    print(f'    sample row={r} iv={iv}: hex={raw.hex()}  <b?={list(raw)}  <iib?={struct.unpack_from("<i", raw, 0)[0]}')
# Wait let's check exact byte layout of TCrs 10B from 0x155a320 in disasm_recon12!
# Earlier in recon12: PUnI, PUnT, PUnP, PUnJ! Let's inspect all 10 bytes statistically!
tc_b = [Counter() for _ in range(10)]
tc_i0 = []; tc_i2 = []; tc_i4 = []
for r, iv, raw in tcrs_items:
    for k in range(10): tc_b[k][raw[k]] += 1
    tc_i0.append(struct.unpack_from('<i', raw, 0)[0])
    tc_i2.append(struct.unpack_from('<i', raw, 2)[0])
    tc_i4.append(struct.unpack_from('<i', raw, 4)[0])
print(f'    distinct per byte [0..9]: {[len(c) for c in tc_b]}')
print(f'    b[0]={tc_b[0].most_common(8)} b[1]={tc_b[1].most_common(8)} b[8]={tc_b[8].most_common(8)} b[9]={tc_b[9].most_common(8)}')
print(f'    i32@2 min={min(tc_i2)} max={max(tc_i2)} neg={sum(x<0 for x in tc_i2)} | i32@4 min={min(tc_i4)} max={max(tc_i4)} neg={sum(x<0 for x in tc_i4)}')

# 6. Kits (base+0x78):
print(f'\n6. Kits (base+0x78) buckets (kit_type=b22, outfield=b25!=0):')
for k in sorted(kit_by_bucket):
    print(f'    bucket {k}: {kit_by_bucket[k]} items across {len(kit_row_buckets[k])} rows')

# 7. Polymorphic tags 5 (Csoc), 6 (Camc), 7 (Cbbl), 38 (pcpt), 4, 37:
for tg, nm in [(5, 'Csoc'), (6, 'Camc'), (7, 'Cbbl'), (38, 'pcpt'), (4, 'tag4_CCBc'), (37, 'tag37_EPPP')]:
    arr = vtag[tg]
    print(f'\n7. Polymorphic tag {tg} ({nm}): {len(arr)} items across {len(set(r for r,_ in arr))} rows')
    for r, raw in arr[:4]:
        print(f'    sample row={r} len={len(raw)}: hex={raw.hex()}')

# 8. Known club L2 checks (Liverpool ordinal 460; also find Man City / Real Madrid / Bayern via TCht or Cyfn!)
print('\n=== KNOWN CLUB L2 CHECKS ===')
for r in [460]:
    print(f'  row {r} (Liverpool, UID 676): Cyfn={cyfn[r]} Ctlv={ctlv[r]} Cmle={cmle[r]} Cyim={cyim[r]} Cyfb={cyfb[r]} Cytv={cytv[r]} Crcb={crcb[r]} Cown={cown[r]} Csly={csly[r]} Catd={catd[r]} Cmna={cmna[r]} Cmxa={cmxa[r]} TCht={tcht.get(r)!r} Cuf={cuf_map.get(r)}')
# Print top 10 UEFA coeff clubs (by sum of Cuf) with TCht / Cyfn / Catd
top_cuf = sorted(cuf_map.items(), key=lambda kv: sum(kv[1]), reverse=True)[:10]
print('  Top 10 clubs by UEFA coeff sum (ordinal, Cyfn, Catd, Cmxa, TCht, Cuf):')
for r, vals in top_cuf:
    print(f'    ord={r:5d} Cyfn={cyfn[r]:4d} Catd={catd[r]:6d} Cmxa={cmxa[r]:6d} TCht={tcht.get(r,"")!r:20s} Cuf={vals}')
