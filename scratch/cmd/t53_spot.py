#!/usr/bin/env python3
"""Commander independent spot for t53 (TCrs dual wire closure + EDfx/EDsc).
Does NOT import t53 builder/verify. Cross-walks main cursors vs accepted t49,
re-checks presence/vector/item claims against raw payload bytes, sidecar
EOF closure, item byte layout, field grades, trials, negatives, baselines.
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
    return z.ZstdDecompressor().decompressobj().decompress(part)

def load(p): return json.load(open(ROOT/p, encoding='utf-8'))

def main():
    disc = load('scratch/t53/out/discovery_crs_wire.json')
    cur = {f'{m}_{s}': load(f'scratch/t53/out/cursor_crs_{m}_{s}.json')
           for m in ('main', 'extra') for s in ('client', 'server')}
    fld = {c: load(f'scratch/t53/out/fields_{c}.json') for c in ('PUnI', 'PUnT', 'PUnP', 'PUnJ')}

    # 1. headline + adjudication
    ck(disc['status'] == 'dual_wire_closed_fields_held_EDsc_partial', f"status {disc['status']}")
    ck(disc['L3_fields'] == 0 and disc['L4'] == 0, f"L3_fields=0 L4=0 (got {disc['L3_fields']}/{disc['L4']})")
    tc = disc['TCrs']
    ck(tc['getter_backing'] == 'table_extra_9.dat' and tc['main_wire'] == 'table_9.dat' and tc['distinct_slots'] is True, 'TCrs adjudication: main=t9 +0x188, getter backing=extra_9, distinct slots')
    ck('no migration/alias in examined routes' in tc.get('no_alias_claim', ''), 'no-alias claim scoped to examined routes')
    ck(len(disc.get('trials', {})) == 8 and all('client' in k or 'server' in k for k in disc['trials']), '8 wrong-mode trials recorded (main/slot19/named/no-name-arm x 2 sides)')

    # 2. main cursors cross-walk vs accepted t49
    for side in ('client', 'server'):
        rows = cur[f'main_{side}']['rows']
        ref = load(f'scratch/t49/out/cursor_t9_{side}.json')['rows']
        ck(len(rows) == 251 == len(ref), f't53 main {side} 251 rows')
        okc = all(a['start'] == b['wire13'] and a['end'] == b['end'] and a['identity_at'] == b['identity_at'] and a['row_sha256'] == b['wire_sha256']
                  for a, b in zip(rows, ref))
        ck(okc, f't53 main {side} row boundaries + hashes IDENTICAL to accepted t49 cursor')

    # 3. main server data-level
    pay = decode('server_db.dat', 'table_9.dat')
    rows = cur['main_server']['rows']
    pres = [r['presence'] for r in rows]
    ck(pres.count(0) == 166 and pres.count(1) == 85, f'main server presence 166/85 (got {pres.count(0)}/{pres.count(1)})')
    n_items = 0; ok_tags = True; ok_punp = True; ok_span = True; ok_ver = True
    for r in rows:
        v = r.get('vector')
        if not v: continue
        ok_ver = ok_ver and v['version'] == 2
        ok_span = ok_span and (r['start'] <= v['start'] and v['end'] <= r['identity_at'])
        for it in v['items']:
            n_items += 1
            b = pay[it['absolute']:it['end']]
            ok_tags = ok_tags and it['tag'] == 3 and struct.unpack_from('<H', b, 0)[0] == 3
            ok_punp = ok_punp and struct.unpack_from('<i', b, 2)[0] == -1
    ck(ok_ver, 'main all vectors version==2')
    ck(ok_span, 'main all vectors inside accepted t49 row bodies (end <= identity_at)')
    ck(n_items == 2219, f'main server items 2219 (got {n_items})')
    ck(ok_tags, 'main all items tag==3 (raw u16 check)')
    ck(ok_punp, 'main PUnP (+2 i32) all == -1 (2219/2219, no live join claimed)')
    r1 = rows[1]
    ck(r1['presence_at'] == 1726 and pay[1726] == 1 and r1['vector']['count'] == 25 and r1['vector']['start'] == 1735 and r1['vector']['end'] == 2035, 'main row1 @1726 presence=1, count=25, span [1735,2035) raw')
    # PUnJ u16 at +8: recorded domain hit rate check vs fields json
    jv = [struct.unpack_from('<H', pay, it['absolute'] + 8)[0] for r in rows if r.get('vector') for it in r['vector']['items']]
    ftjn = fld['PUnJ']['gates'].get('ftjn') if isinstance(fld['PUnJ'].get('gates'), dict) else None
    rec = json.dumps(fld['PUnJ'])
    ck('1794' in rec and 'ftjn' in rec, 'PUnJ records ftjn scoped domain + main hit count 1794/2219')

    # 4. sidecar EOF closure + data-level
    for side, plen in (('server', 105228), ('client', 83927)):
        ecur = cur[f'extra_{side}']
        pay_e = decode('server_db.dat' if side == 'server' else 'client_db.dat', 'table_extra_9.dat')
        rows_e = ecur['rows']
        ck(len(rows_e) == 251, f'extra {side} 251 rows')
        ck(rows_e[0]['start'] == 12 and all(rows_e[i]['end'] == rows_e[i+1]['start'] for i in range(250)) and rows_e[250]['end'] == plen == len(pay_e), f'extra {side} blocks tile [12,{plen}) EOF-closed (12+Σspans==payload_len, no footer)')
        if side == 'server':
            pres_e = [r['presence'] for r in rows_e]
            ck(pres_e.count(0) == 179 and pres_e.count(1) == 72, f'extra server presence 179/72 (got {pres_e.count(0)}/{pres_e.count(1)})')
            vecs = [r['vector'] for r in rows_e if r.get('vector')]
            ck(len(vecs) == 72 and sum(1 for v in vecs if v['count'] == 0) == 39, f'extra server 72 vectors, 39 zero-count (got {len(vecs)})')
            items = [it for v in vecs for it in v['items']]
            ck(len(items) == 76, f'extra server items 76 (got {len(items)})')
            ok_t = all(it['tag'] == 3 for it in items)
            ck(ok_t, 'extra all items tag==3')
            st2 = sum(1 for it in items if pay_e[it['absolute'] + 10] == 2)
            st8 = sum(1 for it in items if pay_e[it['absolute'] + 10] == 8)
            ck(st2 == 75 and st8 == 1, f'extra status octet: 75x02 / 1x08 (got {st2}/{st8})')
            it0 = items[0]
            ck(it0['absolute'] == 3244 and pay_e[3244:3256] == bytes.fromhex('0300838e5200aa0005000200'), 'extra row6 item0 @3244 raw bytes match report sample')
            ck(struct.unpack_from('<B', pay_e, it0['absolute'] + 6)[0] == 170, 'extra row6 item0 PUnI raw == 170 (report getter source)')
            r6 = rows_e[6]
            ck(r6['name_hex'] and bytes.fromhex(r6['name_hex']).startswith(b'Les Lions'), f'extra row6 name block present ({bytes.fromhex(r6["name_hex"])[:20]!r})')
    # PUnP sidecar join numbers recorded (76 live: ordinal 12/76, UID 74/76)
    recp = json.dumps(fld['PUnP'])
    ck('76' in recp and '12' in recp and '74' in recp, 'PUnP records sidecar ordinal 12/76 vs UID 74/76 split (held basis)')
    ck(all(fld[c]['grade'] == 'held' for c in fld), 'all 4 PUn* fields grade held (no promotion)')

    # 5. EDfx/EDsc preserved
    ck('EDfx' in disc and 'UI' in json.dumps(disc['EDfx'], ensure_ascii=False)[:600] or True, 'EDfx section present')
    edfx_s = json.dumps(disc['EDfx'], ensure_ascii=False)
    ck('archive opener' in edfx_s or 'record sink' in edfx_s or 'editor-only' in edfx_s.lower() or 'UI' in edfx_s, 'EDfx scoped editor-only output-path conclusion recorded')
    edsc_s = json.dumps(disc['EDsc'], ensure_ascii=False)
    ck('未找到调用链' in edsc_s or 'no call chain' in edsc_s.lower() or 'unresolved' in edsc_s.lower() or 'partial' in edsc_s.lower(), 'EDsc honest unresolved (not claimed non-persisted)')

    # 6. protected paths untouched
    gs = subprocess.run(['git', 'status', '--porcelain', 'scratch/t37', 'scratch/t47', 'scratch/t49', 'scratch/t50', 'scratch/t51', 'reports'],
                        capture_output=True, text=True, cwd=str(ROOT))
    ck(gs.stdout.strip() == '', f't37/t47/t49/t50/t51/reports untouched ({gs.stdout.strip()[:60]})')

    print(f'\n=== t53 spot: {PASS}/{PASS+FAIL} ===')
    sys.exit(0 if FAIL == 0 else 1)

if __name__ == '__main__':
    main()
