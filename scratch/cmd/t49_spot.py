#!/usr/bin/env python3
"""Commander independent spot for t49 (t9 NATIONAL_TEAM_CONTAINER dual-mode wire).
Does NOT import t49 builder/verify. Re-decodes table_9/table_extra_9 payloads
independently via the read-only codec, checks cursor coordinates against raw
bytes, cross-archive item-byte equality, count distributions, field domains,
grade sums, baseline SHAs, and re-runs worker checks as subprocesses.
"""
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import struct
import subprocess
import sys

ROOT = Path('D:/tmp2b/fm24-db')
DATA = Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
CODEC = ROOT.parent/'fm24/scripts/modding_read_dbdat.py'
ENV = dict(os.environ, FM24_DB_DIR=str(DATA))
PASS = FAIL = 0

def ck(ok, msg):
    global PASS, FAIL
    if ok: PASS += 1; print(f'[PASS] {msg}')
    else: FAIL += 1; print(f'[FAIL] {msg}')

def H(b): return sha256(b).hexdigest()

def decode(archive, member):
    ind = runpy.run_path(str(CODEC))
    z = ind['_zstd_module']()
    _, blob, d = ind['_entries'](DATA/archive)
    base = d['data_base']
    e = [x for x in d['entries'] if x['path'].endswith('/'+member)][0]
    st = base + e['offset']; part = blob[st:st+e['packed_size']]
    out = z.ZstdDecompressor().decompressobj().decompress(part)
    return out, part, e

def main():
    disc = json.load(open(ROOT/'scratch/t49/out/discovery_t9_wire.json', encoding='utf-8'))
    cur = {}
    for side in ('client', 'server'):
        cur[side] = json.load(open(ROOT/f'scratch/t49/out/cursor_t9_{side}.json', encoding='utf-8'))
    fld = {}
    for p in ('Nntp','Nctp','Nrtp','NTRv','NWGv','NSps','Nfmp','NCro'):
        fld[p] = json.load(open(ROOT/f'scratch/t49/out/fields_{p}.json', encoding='utf-8'))

    # 1. headline numbers + binding + six rejections
    ck(disc['status'] == 'partial_sidecar_positive_reader_open', f"status {disc['status']}")
    ck(disc['L3'] == 17 and disc['held'] == 13 and disc['L4'] == 0, 'discovery L3=17 held=13 L4=0')
    ck(disc['editor_sha256'].startswith('b82ebe8e032f2017'), 'editor SHA b82ebe8e')
    b = disc['binding']['table_9.dat']
    ck(b['reader'] == 17156880 and b['client_mode'] == 0 and b['server_mode'] == 1, 'binding reader 17156880 client m0 / server m1')
    sb = disc['binding']['table_extra_9.dat']
    ck(sb['reader'] is None and sb.get('may_not_assign_any_target_parent_to_sidecar') is True, 'sidecar unbound + may_not_assign flag')
    nrej = sum(1 for arch in disc['trials'].values() for mem in arch.values() for m in mem.values() if m['first_failure'])
    ntot = sum(len(mem) for arch in disc['trials'].values() for mem in arch.values())
    ck(ntot == 8 and nrej == 6, f'trials: {ntot} member/mode combos, {nrej} rejections')

    # 2. independent payload decode of 4 members
    pl = {}
    for side, arch in (('client','client_db.dat'), ('server','server_db.dat')):
        for mem, size in (('table_9.dat', None), ('table_extra_9.dat', None)):
            out, part, e = decode(arch, mem)
            rec = disc['archives'][side]['members'][mem]
            key = f'{side}/{mem}'
            pl[key] = out
            ck(rec['payload_size'] == len(out) == e['size'], f'{key} size {len(out)} == entry.size == recorded')
            ck(H(out) == rec['payload_sha256'], f'{key} payload SHA matches recorded {H(out)[:16]}')
            ck(H(part) == rec['entry']['sha256'], f'{key} compressed region SHA matches entry {H(part)[:16]}')
            ck(out[:8] == bytes.fromhex('03017461642ef10d'), f'{key} tad shell')
            ck(struct.unpack_from('<I', out, 8)[0] == 251 == rec['header_count'], f'{key} count@8==251')
    ck(len(pl['client/table_9.dat']) == 31956 and len(pl['server/table_9.dat']) == 307564, 'table_9 sizes 31956/307564')
    ck(len(pl['client/table_extra_9.dat']) == 83927 and len(pl['server/table_extra_9.dat']) == 105228, 'table_extra_9 sizes 83927/105228')

    # 3. cursor arithmetic vs raw bytes (table_9 both sides)
    FOOT = b'\x00'*4 + b'\x01' + bytes.fromhex('ec7ae404')
    for side in ('client', 'server'):
        c = cur[side]; pay = pl[f'{side}/table_9.dat']
        ck(c['mode'] == (0 if side=='client' else 1), f'{side} cursor mode')
        ck(c['row_count'] == 251 and len(c['rows']) == 251, f'{side} 251 rows')
        ck(c['payload_len'] == len(pay) and H(pay) == c['payload_sha256'], f'{side} cursor payload SHA/len match')
        tot = sum(r['length'] for r in c['rows'])
        ck(13 + tot + 9 == len(pay), f'{side} closure 13+{tot}+9=={len(pay)}')
        ck(all(r['selector'] == 0 for r in c['rows']), f'{side} all selectors 0')
        ck(all(pay[r['wire13']] == 0 for r in c['rows']), f'{side} raw selector byte 0 at every wire13')
        ck(all(r['identity_at'] == r['end'] - 12 for r in c['rows']), f'{side} identity tail = last 12B of every row')
        ck(pay[len(pay)-9:] == FOOT, f'{side} footer 00000000|01|ec7ae404 at {len(pay)-9}')
        r0 = c['rows'][0]
        ck(struct.unpack_from('<III', pay, r0['identity_at']) == (0, 5, 5), f'{side} row0 identity (0,5,5) at {r0["identity_at"]}')
        ck(H(pay[r0['wire13']:r0['end']]) == r0['wire_sha256'], f'{side} row0 wire_sha256 recompute')
        trials_side = disc['trials'][side]['table_9.dat']
        okmode = str(c['mode']) in trials_side and trials_side[str(c['mode'])]['closed'] is True
        badmode = [m for m, v in trials_side.items() if v['first_failure']]
        ck(okmode and str(1 - c['mode']) in badmode, f'{side} bound mode closed, opposite mode has first_failure')

    # 4. data-level field checks on server table_9
    pay_s = pl['server/table_9.dat']; pay_c = pl['client/table_9.dat']
    cs = cur['server']['rows']; cc = cur['client']['rows']
    # NCro: every row gate 0, no live items
    gates = [r['collections']['NCro'] for r in cs]
    ck(all((g['gate'] is not None and g['gate'][1] == 0 and g['count'] is None) for g in gates), 'NCro all 251 rows gate=0, no count')
    # count distributions repu trio
    for name, n20, n0 in (('NTRv', 114, 137), ('NWGv', 114, 137), ('NSps', 18, 233)):
        counts = [r['collections'][name]['count'] for r in cs]
        ck(counts.count(20) == n20 and counts.count(0) == n0 and sum(counts) == n20*20, f'{name} server counts: {n20}x20+{n0}x0, items {sum(counts)}')
        nul = [(r['collections'].get(name) or {}).get('count') for r in cc]
        ck(all(v is None for v in nul), f'{name} client mode bypass (no collection)')
    # Nntp/Nctp/Nrtp totals + cross-archive item byte equality + domains
    for name, expect, stride in (('Nntp', 1136, 9), ('Nctp', 640, 8), ('Nrtp', 254, 8)):
        ssum = sum(r['collections'][name]['count'] or 0 for r in cs)
        csum = sum(r['collections'][name]['count'] or 0 for r in cc)
        ck(ssum == csum == expect, f'{name} items client==server=={expect} (got {csum}/{ssum})')
        cmp_items = mism = 0
        for rc_, rs in zip(cc, cs):
            a = rc_['collections'][name]; bq = rs['collections'][name]
            if a['count'] and bq['count'] and a['count'] == bq['count']:
                sa = pay_c[a['start']:a['start']+a['count']*stride]
                sbb = pay_s[bq['start']:bq['start']+bq['count']*stride]
                cmp_items += a['count']
                if sa != sbb: mism += 1
        ck(mism == 0 and cmp_items == expect, f'{name} cross-archive item bytes equal for {cmp_items} items, {mism} row mismatches')
        # nati/cont/regi first-lane i32 in target ordinal range on server
        vals = []
        for r in cs:
            col = r['collections'][name]
            if col['count']:
                for j in range(col['count']):
                    vals.append(struct.unpack_from('<i', pay_s, col['start'] + j*stride)[0])
        ck(all(0 <= v < 251 for v in vals), f'{name} first-lane i32 all in [0,250] ({len(vals)} items, min {min(vals)}, max {max(vals)})')
    # Nfmp: row0 pers=43016, side/perm byte 0x0c, perm distribution
    r0 = cs[0]['collections']['Nfmp']
    ck(r0['count'] == 26 and r0['start'] == 284, f'Nfmp server row0 count 26 start 284 (got {r0["count"]}/{r0["start"]})')
    ck(struct.unpack_from('<i', pay_s, r0['start'])[0] == 43016, 'Nfmp row0 item0 pers @284 == 43016')
    ck(pay_s[r0['start']+7] == 0x0c, 'Nfmp row0 item0 side/perm byte @291 == 0c (side=4, perm=1)')
    ones = zeros = 0; side_vals = set(); pers_miss = []
    for r in cs:
        col = r['collections']['Nfmp']
        if col['count']:
            for j in range(col['count']):
                st_ = col['start'] + j*9
                pv = (pay_s[st_+7] >> 3) & 1
                ones += pv; zeros += (1 - pv)
                side_vals.add(pay_s[st_+7] & 0x07)
    ck(ones == 1731 and zeros == 927, f'Nfmp perm bits ones/zeros {ones}/{zeros} (perm0=927, perm1=1731)')
    ck(side_vals <= set(range(8)), f'Nfmp side values subset of 0..7 (obs {sorted(side_vals)})')
    # NTRv/NWGv/NSps valu i32 sanity on server
    for name in ('NTRv', 'NWGv', 'NSps'):
        vs = []
        for r in cs:
            col = r['collections'][name]
            if col['count']:
                for j in range(col['count']):
                    vs.append(struct.unpack_from('<i', pay_s, col['start'] + j*4)[0])
        ck(len(vs) == sum(r['collections'][name]['count'] or 0 for r in cs), f'{name} valu items decoded {len(vs)}')
        ck(min(vs) >= 0, f'{name} valu i32 all nonneg (min {min(vs)}, max {max(vs)})')

    # 5. grade sums from fields_*.json
    exp_L3 = {'Nntp':3,'Nctp':4,'Nrtp':4,'NTRv':1,'NWGv':1,'NSps':1,'Nfmp':3,'NCro':0}
    exp_held = {'Nntp':3,'Nctp':1,'Nrtp':1,'NTRv':1,'NWGv':1,'NSps':1,'Nfmp':3,'NCro':2}
    for p in exp_L3:
        ck(fld[p]['L3'] == exp_L3[p] and fld[p]['L4'] == 0, f'{p} L3={exp_L3[p]} L4=0')
        nh = sum(1 for fd in fld[p]['fields'].values() if fd.get('grade') == 'held')
        ck(nh == exp_held[p], f'{p} held={exp_held[p]} (got {nh})')
    ck(sum(exp_L3.values()) == 17 and sum(exp_held.values()) == 13, 'grade sums 17 L3 + 13 held')

    # 6. baselines untouched
    ck(H((ROOT/'scratch/t37/out/nation_subtable_inventory.json').read_bytes()).startswith('8af89c72'), 't37 inventory SHA 8af89c72 untouched')
    ck(H((ROOT/'scratch/t47/out/discovery_nation_unknown.json').read_bytes()).startswith('2c0a5b53'), 't47 discovery SHA 2c0a5b53 untouched')

    # 7. worker checks as subprocesses
    rb = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scripts/t49_nation_t9.py'), '--selftest'],
                        capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    ck(rb.returncode == 0 and 'PASS' in (rb.stdout + rb.stderr).upper(), f'builder --selftest rc0 (rc={rb.returncode})')
    rv = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scratch/t49/out/verify.py')],
                        capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    ck(rv.returncode == 0 and 'PASS' in (rv.stdout + rv.stderr).upper(), f't49 verify.py PASS rc0 (rc={rv.returncode})')
    ra = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scripts/t01_anchors.py')],
                        capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    ck(ra.returncode == 0 and '7/7' in ra.stdout, f't01_anchors 7/7 (rc={ra.returncode})')

    print(f'\n=== t49 spot: {PASS}/{PASS+FAIL} ===')
    sys.exit(0 if FAIL == 0 else 1)

if __name__ == '__main__':
    main()
