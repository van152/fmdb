#!/usr/bin/env python3
"""Commander independent spot for t51 (nation 6 unknown parents static discovery).
Does NOT import t51 builder/verify. Re-decodes payloads independently, cross-walks
t51 cursors against accepted t49 (t9) and t47 (t10) row boundaries, checks Nrvn/
Nftb/Calt data-level claims against raw bytes, grade sums, TCrs/EDfx/EDsc negative
preservation, baseline SHAs, and re-runs worker checks as subprocesses.
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
    return out

def load(p): return json.load(open(ROOT/p, encoding='utf-8'))

def main():
    disc = load('scratch/t51/out/discovery_unknown2.json')
    cur = {f'{m}_{s}': load(f'scratch/t51/out/cursor_table_{m}_{s}.json')
           for m in ('9', '10') for s in ('client', 'server')}
    fld = {p: load(f'scratch/t51/out/fields_{p}.json') for p in ('Nrvn', 'Calt', 'Nftb')}

    # 1. headline + per-parent statuses + negative preservation
    ck(disc['status'] == 'partial' and disc['L3'] == 6 and disc['L4'] == 0, f"discovery partial L3=6 L4=0 (got {disc['L3']}/{disc['L4']})")
    par = disc['parents']
    ck(set(par) == {'Nrvn','Calt','TCrs','Nftb','EDfx','EDsc'}, 'exactly the 6 target parents')
    ck(par['Nrvn']['member'] == 'table_9.dat' and par['Nrvn']['status'] == 'cursor_closed' and par['Nrvn']['table_type'] == 9, 'Nrvn -> t9 cursor_closed')
    ck(par['Calt']['member'] == 'table_9.dat' and 'NATIONAL_TEAM_CONTAINER' in str(par['Calt'].get('owner','')), 'Calt -> t9 owner NATIONAL_TEAM_CONTAINER')
    ck(par['Nftb']['member'] == 'table_10.dat' and str(par['Nftb']['status']).startswith('cursor_closed') and par['Nftb']['table_type'] == 10, 'Nftb -> t10 cursor_closed (item fields partial)')
    tcr = par['TCrs']
    ck(str(tcr['status']) != 'cursor_closed' and tcr.get('member') is None, 'TCrs partial, member unbound')
    ne = tcr.get('new_evidence') or {}
    ck(ne.get('object_pointer_path') == [176, 72], 'TCrs counterexample path [+0xb0]+0x48 recorded (0xb0=176, 0x48=72)')
    ck('table_extra_9' in json.dumps(tcr, ensure_ascii=False), 'TCrs table_extra_9 candidate recorded, not bound')
    ck('UI' in json.dumps(par['EDfx'], ensure_ascii=False) or par['EDfx'].get('status') not in ('cursor_closed',), 'EDfx UI-path negative preserved (no archive backing claim)')
    ck(par['EDsc'].get('status') not in ('cursor_closed',), 'EDsc unresolved preserved')

    # 2. independent decode of 6 payloads vs recorded SHAs
    pl = {}
    for side, arch in (('client','client_db.dat'), ('server','server_db.dat')):
        for m in ('table_9.dat', 'table_10.dat', 'table_extra_9.dat'):
            out = decode(arch, m)
            pl[f'{side}/{m}'] = out
            rec = disc['archives'][side]['members'][m]
            ck(len(out) == rec['selected_frame'][2], f'{side}/{m} size {len(out)} == recorded frame')
            ck(H(out) == rec['payload_sha256'], f'{side}/{m} payload SHA matches {H(out)[:16]}')
    ck(len(pl['server/table_10.dat']) == 422345 and H(pl['server/table_10.dat']).startswith('19337841'), 't10 server 422345B SHA 19337841 (cross t46/E85)')
    ck(H(pl['server/table_9.dat']).startswith('6c2d8a06') and H(pl['client/table_9.dat']).startswith('784810f0'), 't9 SHAs cross t49/E89')

    # 3. cross-walk: t51 cursors vs accepted t49 (t9) and t47 (t10) row boundaries
    t49s = load('scratch/t49/out/cursor_t9_server.json')['rows']
    t49c = load('scratch/t49/out/cursor_t9_client.json')['rows']
    for side, ref in (('server', t49s), ('client', t49c)):
        rows = cur[f'9_{side}']['rows']
        ck(len(rows) == 251 == len(ref), f't51 t9 {side} 251 rows == t49 count')
        okc = all(a['wire13'] == b['wire13'] and a['end'] == b['end'] and a['identity_at'] == b['identity_at'] and a['wire_sha256'] == b['wire_sha256']
                  for a, b in zip(rows, ref))
        ck(okc, f't51 t9 {side} row boundaries + row hashes IDENTICAL to accepted t49 cursor (cross-walk)')
    for side in ('server', 'client'):
        ref = load('scratch/t47/out/cursor_nation_tax.json')[side]['rows']
        rows = cur[f'10_{side}']['rows']
        ck(len(rows) == 251 == len(ref), f't51 t10 {side} 251 rows == t47 count')
        okc = all(a['wire13'] == b['wire13'] and a['end'] == b['end'] and a['identity_at'] == b['identity_at'] and a['wire_sha256'] == b['wire_sha256']
                  for a, b in zip(rows, ref))
        ck(okc, f't51 t10 {side} row boundaries + row hashes IDENTICAL to accepted t47 cursor (cross-walk)')

    # 4. Nrvn data-level (server t9 payload)
    pay = pl['server/table_9.dat']
    rows = cur['9_server']['rows']
    nonempty = [r for r in rows if r.get('Nrvn') and r['Nrvn']['count']]
    ck(len(nonempty) == 194 and sum(r['Nrvn']['count'] for r in nonempty) == 720, f'Nrvn 194 non-empty rows, 720 items (got {len(nonempty)}/{sum(r["Nrvn"]["count"] for r in nonempty)})')
    ordvals = []; leves = []; tags_ok = True; kinds_ok = True; inrow_ok = True
    for r in rows:
        n = r.get('Nrvn')
        if not (n and n['count']): continue
        # within accepted t49 row body (before identity tail)
        ref = t49s[r['row']]
        if not (ref['wire13'] <= n['count_at'] and n['end'] <= ref['identity_at']): inrow_ok = False
        if pay[n['count_at']] != n['count']: inrow_ok = False  # Nrvn count is u8 (0x11d1b03)
        for it in n['items']:
            a = it['absolute']
            b = pay[a:a+16]
            tags_ok = tags_ok and b[0xb] == 6
            kinds_ok = kinds_ok and b[0xa] == 2
            ordvals.append(struct.unpack_from('<i', b, 0)[0])
            leves.append(struct.unpack_from('<b', b, 12)[0])
    ck(inrow_ok, 'Nrvn ranges + i16 counts match raw bytes inside accepted t49 row bodies')
    ck(tags_ok and kinds_ok, 'Nrvn all 720 items (kind,tag)=(2,6) in raw bytes')
    ck(all(0 <= v < 251 for v in ordvals), f'Nrvn nati ordinals all in [0,250] ({len(ordvals)} items)')
    ck(all(5 <= v <= 100 for v in leves), f'Nrvn leve all in [5,100] (min {min(leves)}, max {max(leves)})')
    ck(ordvals[0] == 29 and leves[0] == 90, 'Nrvn row0 item0 nati=29 leve=90 (report sample)')
    ck(fld['Nrvn']['L3'] == 2 and fld['Nrvn']['L4'] == 0 and all(fld['Nrvn']['fields'][f]['status'] == 'L3' for f in ('nati', 'leve')), 'Nrvn L3=2 (nati,leve)')
    j = fld['Nrvn']['fields']['nati']['join']
    ck(j['live'] == 720 and j['ordinal_matches'] == 720, 'Nrvn nati join 720/720 ordinals')

    # 5. Nftb data-level (server t10 payload)
    pay10 = pl['server/table_10.dat']
    rows10 = cur['10_server']['rows']
    ne = [r for r in rows10 if r.get('Nftb') and r['Nftb']['count']]
    ck(len(ne) == 1 and ne[0]['row'] == 162 and ne[0]['Nftb']['count'] == 7, 'Nftb exactly one non-empty row (row 162, count 7)')
    ck(struct.unpack_from('<h', pay10, ne[0]['Nftb']['count_at'])[0] == 7, 'Nftb i16 count@278809 == 7 in raw bytes')
    lens = [it['length'] for it in ne[0]['Nftb']['items']]
    ck(all(46 <= L <= 54 for L in lens) and len(lens) == 7, f'Nftb 7 item lengths 46-54 (got {lens})')
    ck(all(it['tag'] == 1 for it in ne[0]['Nftb']['items']), 'Nftb all 7 items tag=1')
    it0 = ne[0]['Nftb']['items'][0]
    ck(it0['date']['absolute'] == 278844 and pay10[278844:278848] == bytes.fromhex('2700b607'), 'Nftb item0 packed date @278844 == 2700b607')
    empty_cn = sum(1 for it in ne[0]['Nftb']['items'] if it['strings'][3][1] == 0)
    ck(empty_cn == 7, 'Nftb NbCn (string idx3) zero-length in all 7 items')
    s0 = it0['strings'][0]
    ck(s0[1] == 5 and bytes.fromhex(s0[2]) == b'Bruno', 'Nftb item0 NpFn == "Bruno" (5B) raw check')
    ref = [r for r in load('scratch/t47/out/cursor_nation_tax.json')['server']['rows'] if r['row'] == 162][0]
    ck(ref['wire13'] <= ne[0]['Nftb']['count_at'] and ne[0]['Nftb']['items'][-1]['end'] <= ref['identity_at'], 'Nftb items inside accepted t47 t10 row 162 body')
    grades = {k: v['status'] for k, v in fld['Nftb']['fields'].items()}
    ck(sum(1 for v in grades.values() if v == 'L3') == 4, f'Nftb L3 fields == 4 ({grades})')
    ck(sum(1 for v in grades.values() if v == 'held') == 3, f'Nftb held == 3 (NbPi/NbPn/NbFt)')

    # 6. Calt zero-count + held
    ck(all((r.get('Calt') or {}).get('count') == 0 for r in rows), 'Calt all 251 server rows count 0')
    ck(pl['server/table_9.dat'][1097:1099] == b'\x00\x00', 'Calt row0 count @1097 == 0000 raw')
    ck(fld['Calt']['L3'] == 0 and all(fld['Calt']['fields'][f]['status'] == 'held' for f in ('cmid', 'stid')), 'Calt cmid/stid held (0 live)')
    ck(disc['L3'] == 6 == 2 + 4 and fld['Nrvn']['L3'] + fld['Nftb']['L3'] == 6, 'grade sums: L3 6 == Nrvn 2 + Nftb 4')

    # 7. baselines untouched (git working tree clean for protected paths)
    gs = subprocess.run(['git', 'status', '--porcelain', 'scratch/t37', 'scratch/t47', 'scratch/t49', 'reports', 'prompts'],
                        capture_output=True, text=True, cwd=str(ROOT))
    ck(gs.stdout.strip() == '', f't37/t47/t49/reports/prompts untouched in worktree ({gs.stdout.strip()[:80]})')

    # 8. worker checks as subprocesses
    rb = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scripts/t51_nation_unknown2.py'), '--selftest'],
                        capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    ck(rb.returncode == 0 and 'PASS' in (rb.stdout + rb.stderr).upper(), f'builder --selftest rc0 (rc={rb.returncode})')
    rv = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scratch/t51/out/verify.py')],
                        capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    ck(rv.returncode == 0 and 'PASS' in (rv.stdout + rv.stderr).upper(), f't51 verify.py PASS rc0 (rc={rv.returncode})')
    ra = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scripts/t01_anchors.py')],
                        capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    ck(ra.returncode == 0 and '7/7' in ra.stdout, f't01_anchors 7/7 (rc={ra.returncode})')

    print(f'\n=== t51 spot: {PASS}/{PASS+FAIL} ===')
    sys.exit(0 if FAIL == 0 else 1)

if __name__ == '__main__':
    main()
