"""Disasm Cspb(0x3ea5150), Cren(0x11d4590), TCrs(0x4387ab0) + full-archive exact item-level domain audit
for ALL 16 list fields in table_extra_3.dat + real target table UID/ordinal cross-checks."""
import json, os, struct, sys
from collections import Counter
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
pe = pefile.PE(data=PE, fast_load=True); IB = pe.OPTIONAL_HEADER.ImageBase
va = lambda fo: IB + pe.get_rva_from_offset(fo)
md = capstone.Cs(capstone.CS_ARCH_X86, capstone.CS_MODE_64)

def dump(name, fo, sz):
    print(f'=== {name} @ 0x{fo:x} (VA 0x{va(fo):x}) ===')
    sva = va(fo)
    for ins in md.disasm(PE[fo:fo+sz], sva):
        cfo = ins.address - sva + fo
        print(f'  0x{cfo:x}: {ins.mnemonic:8s} {ins.op_str}')
        if ins.mnemonic == 'ret' and PE[cfo+ins.size] in (0xcc, 0x90): break

dump('CSPB_ITEM_RDR_0x3ea5150', 0x3ea5150, 0x1e0)
dump('CREN_INLINE_RDR_0x11d4590', 0x11d4590, 0xd0)
dump('TCRS_ITEM_RDR_0x4387ab0', 0x4387ab0, 0x260)

# Extract FMF members
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
N = struct.unpack_from('<I', srv_ex3, 8)[0]

# Extract ALL comp UIDs from client_db/table_25.dat (stride 126B: 13 + 7047*126 + 9 = 887944? Wait len=894991 -> 894991-22=894969 / 7047 = 127!)
t25 = cli_get('client_db/table_25.dat')
cnt25 = struct.unpack_from('<I', t25, 8)[0]
assert (len(t25) - 22) % cnt25 == 0
stride25 = (len(t25) - 22) // cnt25
# In table_25 client rows, identity is last 12 bytes before next selector (same as stadium/club!)
# Let's check exact identity offset in row 0 & row 1 of client table_25!
comp_uids = set()
comp_ord_to_uid = {}
for off in range(0, stride25 - 12):
    if struct.unpack_from('<I', t25, 13 + off)[0] == 0 and struct.unpack_from('<I', t25, 13 + stride25 + off)[0] == 1 and struct.unpack_from('<I', t25, 13 + 2*stride25 + off)[0] == 2:
        # check u1 == u2
        u1, u2 = struct.unpack_from('<II', t25, 13 + off + 4)
        if u1 == u2 and u1 > 0:
            print(f'\n[table_25 client] stride={stride25}, id_off={off}, row0_uid={u1}')
            for k in range(cnt25):
                o, u1, u2 = struct.unpack_from('<III', t25, 13 + k*stride25 + off)
                assert o == k and u1 == u2
                comp_uids.add(u1); comp_ord_to_uid[k] = u1
            break

# Extract ALL stage_name UIDs from server_db/table_29.dat? Wait check which table is stage_name!
# Check db_tables_big or check table_29 stride or check which table has stage_name UID 97 (0x61)!
for tnum in range(0, 80):
    rel = f'server_db/table_{tnum}.dat'
    if rel not in srv_ent: continue
    buf = srv_get(rel)
    cnt = struct.unpack_from('<I', buf, 8)[0]
    if cnt == 0: continue
    if (len(buf) - 22) % cnt == 0:
        st = (len(buf) - 22) // cnt
        if st >= 13 and cnt >= 2:
            for off in range(0, st - 12):
                if struct.unpack_from('<I', buf, 13 + off)[0] == 0 and struct.unpack_from('<I', buf, 13 + st + off)[0] == 1:
                    u1, u2 = struct.unpack_from('<II', buf, 13 + off + 4)
                    if u1 == u2 and u1 > 0:
                        if tnum in (25, 29, 32, 39, 44, 45, 51, 52, 53, 54, 55, 56, 57, 58, 60, 61):
                            print(f'  [srv table_{tnum}] cnt={cnt} stride={st} id_off={off} row0_uid={u1}')
                        break

# Check stage_name table via editor.exe RTTI DATABASE_TABLE<STAGE_NAME>!
sn_pos = PE.find(b'.?AV?$DATABASE_TABLE@VSTAGE_NAME@db@@@db@@')
if sn_pos != -1:
    td_rva = pe.get_rva_from_offset(sn_pos - 16)
    p0 = 0
    while True:
        idx = PE.find(struct.pack('<I', td_rva), p0)
        if idx == -1: break
        if idx >= 12 and struct.unpack_from('<I', PE, idx-12)[0] == 1:
            col_va = va(idx - 12)
            cp = PE.find(struct.pack('<Q', col_va))
            if cp != -1:
                vt_va = va(cp + 8)
                # find lea in 0xf02000..0xf0a000
                for ins in md.disasm(PE[0xf02000:0xf0a000], va(0xf02000)):
                    if ins.mnemonic == 'lea' and 'rip' in ins.op_str:
                        import re
                        m = re.search(r'rip ([+-]) 0x([0-9a-f]+)', ins.op_str)
                        if m:
                            s = 1 if m.group(1) == '+' else -1
                            if ins.address + ins.size + s * int(m.group(2), 16) == vt_va:
                                hfo = pe.get_offset_from_rva(ins.address - IB)
                                print(f'  [STAGE_NAME table init @ 0x{hfo:x}]')
                                for ins2 in md.disasm(PE[hfo-0x20:hfo+0x10], va(hfo-0x20)):
                                    print(f'    0x{pe.get_offset_from_rva(ins2.address-IB):x}: {ins2.mnemonic} {ins2.op_str}')
        p0 = idx + 4

# Check basic_people_db.dat person UIDs! Wait basic_people_db.dat has 658,011 people!
pb_raw = (DATA / 'basic_people_db.dat').read_bytes()
pb_dec = zstd.ZstdDecompressor().decompressobj().decompress(pb_raw[8:])
p_cnt = struct.unpack_from('<I', pb_dec, 0)[0]
print(f'\n[basic_people_db] len={len(pb_dec)}, cnt={p_cnt}, (len-4)/cnt={(len(pb_dec)-4)/p_cnt:.4f}')
# Also check people_db.dat!
pdb_raw = (DATA / 'people_db.dat').read_bytes()
print(f'  [people_db.dat] first 24B={pdb_raw[:24].hex()}')
# Check if basic_people_db has fixed stride? 54060043 - 4 = 54060039, / 658011 = 82.1567 (variable length!)
# Wait: check pl_hist_id.dat or non_pl_hist_id.dat? No, we don't need to guess person layout if we check whether CPsL/Cbbl/Csoc/Camc/pcpt/Cren/TCrs person IDs are positive UIDs vs ordinals!

# Full replay of ALL 16 list fields with EXACT verified layouts!
master = json.loads((ROOT / 'evidence/fm24/reports/editor_schema/master.json').read_bytes())
ftjn_vals = set(int(v['enum']) for v in master['enums']['ftjn']['values'])

def date4_ok(u):
    yr = (u >> 16) & 0xffff; doy = u & 0x1ff; mid = (u >> 9) & 0x7f
    leap = 1 if (yr % 4 == 0 and (yr % 100 != 0 or yr % 400 == 0)) else 0
    return (yr >= 1) and (1 <= doy <= 365 + leap) and (mid == 0), (u == 0x076c0001)

cscm = []; cpsl = []; cspb = []; cren = []; tcrs = []
csoc = []; camc = []; cbbl = []; pcpt = []; kits = []

p = 12
for i in range(N):
    o = struct.unpack_from('<I', srv_ex3, p)[0]; p += 4
    p += 3
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
        # 1B ver + 8B stco(u1,u2) + 1B stnm(i8) + 8B slsn(u1,u2) + 4B tail
        ver, co1, co2, stnm, sn1, sn2, tl = struct.unpack_from('<Bii bii i'.replace(' ', ''), srv_ex3, p)
        cscm.append((i, ver, co1, co2, stnm, sn1, sn2, tl)); p += 22
    c20 = srv_ex3[p]; p += 1 + 10 * c20
    f48 = srv_ex3[p]; p += 1
    if f48:
        t48 = struct.unpack_from('<b', srv_ex3, p)[0]; p += 1
        p += (24 if t48 > 0 else 16)
        cnt48 = srv_ex3[p]; p += 1 + 4 * cnt48
    p += 7
    c68 = struct.unpack_from('<H', srv_ex3, p)[0]; p += 2
    for _ in range(c68):
        tg, p1, p2, w8 = struct.unpack_from('<BiiH', srv_ex3, p)
        cpsl.append((i, tg, p1, p2, w8)); p += 11
    p += 3
    # common tail
    p += 8
    tlen = struct.unpack_from('<I', srv_ex3, p)[0]; p += 4 + tlen
    kcnt = srv_ex3[p]; p += 1
    for _ in range(kcnt):
        kits.append((i, srv_ex3[p:p+27])); p += 27
    p += 8
    # server tail
    c18b = struct.unpack_from('<h', srv_ex3, p)[0]; p += 2
    for _ in range(c18b):
        # Wait verify from 0x3ea5150 above! Temporarily store raw
        cspb.append((i, srv_ex3[p:p+20])); p += 20
    c30b = struct.unpack_from('<b', srv_ex3, p)[0]; p += 1
    for _ in range(c30b):
        cren.append((i, srv_ex3[p:p+6])); p += 6
    p += 16
    cb0 = struct.unpack_from('<H', srv_ex3, p)[0]; p += 2
    for _ in range(cb0):
        t = srv_ex3[p]; p += 1
        sp = p
        if t == 5:
            # 0x42d2710: +8(8B play u1,u2), +10(4B club ord!), +21(1B perc i8), +20(1B), +18(4B), +1c(4B), +22(1B), +23(1B)
            p1, p2, club_ord, perc, b20, d18, d1c, b22, b23 = struct.unpack_from('<iiibbiiBB', srv_ex3, p)
            csoc.append((i, p1, p2, club_ord, perc, b20, d18, d1c, b22, b23))
            p += 24
        elif t == 6:
            # 0x42d6a10: +8(8B play u1,u2), +10(4B club ord), +18(4B cash), +1c(1B apps), +1d(1B apfr), +1e(1B type)
            p1, p2, club_ord, cash, apps, apfr, ctype = struct.unpack_from('<iiiibbb', srv_ex3, p)
            camc.append((i, p1, p2, club_ord, cash, apps, apfr, ctype))
            p += 19
        elif t == 7:
            # 0x42c66f0: +10(8B play u1,u2), +18(4B cash), +20(4B club ord), +8(4B bbsd), +c(4B bbed)
            p1, p2, cash, club_ord, bbsd, bbed = struct.unpack_from('<iiiiII', srv_ex3, p)
            cbbl.append((i, p1, p2, cash, club_ord, bbsd, bbed))
            p += 24
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
                # 0x14da650: 1B ver, 4B vec_cnt(0), 4B +30(PtPl), 4B +34(date1), 4B +38(PtLy), 2B +3c, 4B+str
                ver = srv_ex3[p]; m38 = struct.unpack_from('<I', srv_ex3, p+1)[0]
                ptpl, d1, ptly, w3c = struct.unpack_from('<iIIH', srv_ex3, p+5)
                sl = struct.unpack_from('<I', srv_ex3, p+19)[0]
                sstr = srv_ex3[p+23:p+23+sl]
                pcpt.append((i, ver, m38, ptpl, d1, ptly, w3c, sstr))
                p += 23 + sl
    f48b = srv_ex3[p]; p += 1
    if f48b:
        v48, c48 = struct.unpack_from('<II', srv_ex3, p); p += 8
        for _ in range(c48):
            iv = struct.unpack_from('<h', srv_ex3, p)[0]; p += 2
            sz = 8 + (iv >= 2) + (iv >= 3)
            tcrs.append((i, iv, srv_ex3[p:p+sz])); p += sz
assert p == len(srv_ex3)

print('\n=== FULL ITEM-LEVEL AUDIT ===')
# 1. Cscm
print(f'\n[Cscm] total={len(cscm)} items across {len(set(x[0] for x in cscm))} rows')
print('  ver:', Counter(x[1] for x in cscm))
co_miss = [x for x in cscm if x[2] != -1 and x[2] not in comp_uids]
co_ne = [x for x in cscm if x[2] != x[3]]
stnm_vals = [x[4] for x in cscm]
stnm_viol = [x for x in cscm if x[4] < 0 or x[4] > 200]
sn_ne = [x for x in cscm if x[5] != x[6]]
sn_vals = [x[5] for x in cscm]
print(f'  stco: eq_pair={len(cscm)-len(co_ne)}/{len(cscm)}, null(-1)={sum(x[2]==-1 for x in cscm)}, in_comp_uids_miss={len(co_miss)} (first={co_miss[:3]})')
print(f'  stnm: min={min(stnm_vals)} max={max(stnm_vals)} neg={sum(v<0 for v in stnm_vals)} viol_0_200={len(stnm_viol)} (first={stnm_viol[:3]})')
print(f'  slsn: eq_pair={len(cscm)-len(sn_ne)}/{len(cscm)}, null(-1)={sum(x[5]==-1 for x in cscm)}, min_nz={min(v for v in sn_vals if v!=-1)} max={max(sn_vals)} distinct={len(set(sn_vals))}')
print(f'  tail4: {Counter(x[7] for x in cscm).most_common(5)}')

# 2. CPsL
print(f'\n[CPsL] total={len(cpsl)} items across {len(set(x[0] for x in cpsl))} rows')
print(f'  tag={Counter(x[1] for x in cpsl)}, w8={Counter(x[4] for x in cpsl)}')
print(f'  per1: min={min(x[2] for x in cpsl)} max={max(x[2] for x in cpsl)} neg={sum(x[2]<0 for x in cpsl)}')
print(f'  per2: min={min(x[3] for x in cpsl)} max={max(x[3] for x in cpsl)} neg={sum(x[3]<0 for x in cpsl)}')

# 3. Csoc (tag 5)
print(f'\n[Csoc tag 5] total={len(csoc)} items across {len(set(x[0] for x in csoc))} rows')
cs_play_ne = sum(x[1] != x[2] for x in csoc)
cs_club_bad = [x for x in csoc if x[3] != -1 and not (0 <= x[3] < 84259)]
cs_perc_bad = [x for x in csoc if not (0 <= x[4] <= 100)]
print(f'  play: eq_pair={len(csoc)-cs_play_ne}/{len(csoc)} min={min(x[1] for x in csoc)} max={max(x[1] for x in csoc)} neg={sum(x[1]<0 for x in csoc)}')
print(f'  club(ord): min={min(x[3] for x in csoc)} max={max(x[3] for x in csoc)} null(-1)={sum(x[3]==-1 for x in csoc)} oob={len(cs_club_bad)} first={cs_club_bad[:3]}')
print(f'  perc: min={min(x[4] for x in csoc)} max={max(x[4] for x in csoc)} viol_0_100={len(cs_perc_bad)} first={cs_perc_bad[:3]}')
print(f'  other bytes: b20={Counter(x[5] for x in csoc).most_common(5)} d18={Counter(x[6] for x in csoc).most_common(5)} d1c={Counter(x[7] for x in csoc).most_common(5)} b22={Counter(x[8] for x in csoc)} b23={Counter(x[9] for x in csoc)}')

# 4. Camc (tag 6)
print(f'\n[Camc tag 6] total={len(camc)} items across {len(set(x[0] for x in camc))} rows')
ca_club_bad = [x for x in camc if x[3] != -1 and not (0 <= x[3] < 84259)]
ca_cash_bad = [x for x in camc if not (0 <= x[4] <= 1000000000)]
ca_apps_bad = [x for x in camc if not (1 <= x[5] <= 100)]
ca_apfr_bad = [x for x in camc if not (1 <= x[6] <= 100)]
print(f'  play: eq_pair={sum(x[1]==x[2] for x in camc)}/{len(camc)} min={min(x[1] for x in camc)} max={max(x[1] for x in camc)} neg={sum(x[1]<0 for x in camc)}')
print(f'  club(ord): min={min(x[3] for x in camc)} max={max(x[3] for x in camc)} null={sum(x[3]==-1 for x in camc)} oob={len(ca_club_bad)}')
print(f'  cash: min={min(x[4] for x in camc)} max={max(x[4] for x in camc)} viol={len(ca_cash_bad)} first={ca_cash_bad[:3]}')
print(f'  apps: min={min(x[5] for x in camc)} max={max(x[5] for x in camc)} viol_1_100={len(ca_apps_bad)} first={ca_apps_bad[:3]}')
print(f'  apfr: min={min(x[6] for x in camc)} max={max(x[6] for x in camc)} viol_1_100={len(ca_apfr_bad)} first={ca_apfr_bad[:3]}')
print(f'  type: {dict(sorted(Counter(x[7] for x in camc).items()))}')

# 5. Cbbl (tag 7)
print(f'\n[Cbbl tag 7] total={len(cbbl)} items across {len(set(x[0] for x in cbbl))} rows')
cb_club_bad = [x for x in cbbl if x[4] != -1 and not (0 <= x[4] < 84259)]
cb_cash_bad = [x for x in cbbl if not (0 <= x[3] <= 1000000000)]
cb_d1_bad = [x for x in cbbl if not date4_ok(x[5])[0]]
cb_d2_bad = [x for x in cbbl if not date4_ok(x[6])[0]]
print(f'  play: eq_pair={sum(x[1]==x[2] for x in cbbl)}/{len(cbbl)} min={min(x[1] for x in cbbl)} max={max(x[1] for x in cbbl)} neg={sum(x[1]<0 for x in cbbl)}')
print(f'  cash: min={min(x[3] for x in cbbl)} max={max(x[3] for x in cbbl)} viol={len(cb_cash_bad)} first={cb_cash_bad[:3]}')
print(f'  club(ord): min={min(x[4] for x in cbbl)} max={max(x[4] for x in cbbl)} null={sum(x[4]==-1 for x in cbbl)} oob={len(cb_club_bad)}')
print(f'  bbsd bad={len(cb_d1_bad)} sent={sum(x[5]==0x076c0001 for x in cbbl)} | bbed bad={len(cb_d2_bad)} sent={sum(x[6]==0x076c0001 for x in cbbl)}')

# 6. pcpt (tag 38)
print(f'\n[pcpt tag 38] total={len(pcpt)} items across {len(set(x[0] for x in pcpt))} rows')
pc_d1_bad = [x for x in pcpt if not date4_ok(x[4])[0]]
pc_d2_bad = [x for x in pcpt if not date4_ok(x[5])[0]]
print(f'  ver={Counter(x[1] for x in pcpt)} m38={Counter(x[2] for x in pcpt)} w3c={Counter(x[6] for x in pcpt)}')
print(f'  PtPl: min={min(x[3] for x in pcpt)} max={max(x[3] for x in pcpt)} neg={sum(x[3]<0 for x in pcpt)}')
print(f'  d1(date1): bad={len(pc_d1_bad)} sent={sum(x[4]==0x076c0001 for x in pcpt)}')
print(f'  PtLy(date2): bad={len(pc_d2_bad)} sent={sum(x[5]==0x076c0001 for x in pcpt)} years={sorted(set((x[5]>>16)&0xffff for x in pcpt))}')
print(f'  trailing str non-empty: {sum(len(x[7])>0 for x in pcpt)}')
