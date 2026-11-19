#!/usr/bin/env python3
"""Commander independent spot for t50 (t9 data-side profile, L1/L2).
Does NOT import t50 builder/verify or t49/t47 code. Re-decodes payloads,
checks identity census, tiling closure, cross-validates identity-tail
positions against accepted t49/t47 cursors, extra_9 block shape, negatives.
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

def jl(p): return [json.loads(l) for l in open(ROOT/p, encoding='utf-8') if l.strip()]

def main():
    prof = json.load(open(ROOT/'scratch/t50/out/profile_t9.json', encoding='utf-8'))
    gd = json.load(open(ROOT/'scratch/t50/out/grammar_diff_t9.json', encoding='utf-8'))

    # 1. headline
    all_txt = json.dumps(prof) + json.dumps(gd)
    ck('"L3": 0' in all_txt and '"L4": 0' in all_txt, 't50 claims L3=0/L4=0')
    ck("partial" in all_txt, "status honest partial recorded")

    # 2. independent decode of 4 members
    pl = {}
    for side, arch in (('client','client_db.dat'), ('server','server_db.dat')):
        for m in ('table_9.dat', 'table_extra_9.dat'):
            out = decode(arch, m)
            pl[f'{side}/{m}'] = out
            rec = prof['members' if 'members' in prof else 'anchors'][side][m] if isinstance(prof.get('members' if 'members' in prof else 'anchors'), dict) and side in prof.get('members', prof.get('anchors', {})) else None
    anchors = prof.get('anchors') or prof.get('members')
    for side in ('client', 'server'):
        for m in ('table_9.dat', 'table_extra_9.dat'):
            out = pl[f'{side}/{m}']
            a = anchors[side][m] if isinstance(anchors, dict) and side in anchors else None
            if a is None:
                # flatten search
                a = next(v for k, v in (anchors.items() if isinstance(anchors, dict) else [])
                         )  # placeholder, handled below
    # simpler: find anchor records anywhere in prof
    def find_anchor(side, m):
        s = json.dumps(prof)
        # locate by payload sha in any dict
        res = []
        def walk(o):
            if isinstance(o, dict):
                if o.get('payload_sha256') and (m.split('.')[0].replace('table_','') in json.dumps(o)[:400] or True):
                    res.append(o)
                for v in o.values(): walk(v)
            elif isinstance(o, list):
                for v in o: walk(v)
        walk(prof)
        return res

    ck(len(pl['client/table_9.dat']) == 31956 and len(pl['server/table_9.dat']) == 307564, 't9 payload sizes 31956/307564')
    ck(len(pl['client/table_extra_9.dat']) == 83927 and len(pl['server/table_extra_9.dat']) == 105228, 'extra_9 payload sizes 83927/105228')
    ck(H(pl['client/table_9.dat']).startswith('784810f0') and H(pl['server/table_9.dat']).startswith('6c2d8a06'), 't9 SHAs cross t49/E89')
    ck(H(pl['client/table_extra_9.dat']).startswith('2717052d') and H(pl['server/table_extra_9.dat']).startswith('a5671537'), 'extra_9 SHAs cross t49/t51')
    for k, out in pl.items():
        ck(out[:8] == bytes.fromhex('03017461642ef10d') and struct.unpack_from('<I', out, 8)[0] == 251, f'{k} tad shell + count@8==251')

    # 3. t9 rows.jsonl: tiling + identity census
    t49_cur = {}
    for side in ('client', 'server'):
        rows = jl(f'scratch/t50/out/profiles/table_{side}_9.rows.jsonl')
        pay = pl[f'{side}/table_9.dat']
        ck(len(rows) == 251, f't50 t9 {side} 251 rows')
        offs = [r['offset'] for r in rows]
        ck(offs[0] == 13 and all(offs[i] + rows[i]['len'] == offs[i+1] for i in range(250)), f't50 t9 {side} rows tile contiguously from 13')
        ck(offs[250] + rows[250]['len'] == len(pay) - 8, f't50 t9 {side} tiles to payload_len-8 (footer 8)')
        ids = [r['identity'] for r in rows]
        ck([x['ordinal'] for x in ids] == list(range(251)), f't50 t9 {side} ordinals 0..250')
        rids = [x['row_id'] for x in ids]
        ck(all(v != 0 for v in rids) and all(rids[i] < rids[i+1] for i in range(250)) and len(set(rids)) == 251, f't50 t9 {side} row_id nonzero strictly increasing unique')
        ck(all(x['repeated_id'] == x['row_id'] and x['marker'] == 0 for x in ids), f't50 t9 {side} repeated lanes equal, marker 0')
        ck(rids[250] == 82082540 == struct.unpack_from('<I', pay, len(pay)-4)[0], f't50 t9 {side} last row_id == footer u32 82082540')
        # cross-validate identity tail absolute positions vs accepted t49 cursor
        ref = json.load(open(ROOT/f'scratch/t49/out/cursor_t9_{side}.json', encoding='utf-8'))['rows']
        ok_tail = all(rows[i]['offset'] + rows[i]['identity']['tail_offset_in_row'] == ref[i]['identity_at'] for i in range(251))
        ck(ok_tail, f't50 t9 {side} identity tail starts IDENTICAL to accepted t49 identity_at (cross-walk)')
        ok_shift = all(rows[0]['offset'] == ref[0]['wire13'] and rows[i]['offset'] == ref[i]['wire13'] + 1 for i in range(1, 251))
        ck(ok_shift, f't50 t9 {side} body-start shift: t50 offset = t49 wire13 + 1 (i>=1), marker byte attribution documented')
        # repeated-id bytes: raw check on 3 samples
        ok_raw = all(struct.unpack_from('<I', pay, rows[i]['offset'] + rows[i]['identity']['tail_offset_in_row'] + 4)[0] == rows[i]['identity']['row_id'] for i in (0, 125, 250))
        ck(ok_raw, f't50 t9 {side} row_id raw u32 spot at 3 rows')

    # 4. extra_9 blocks
    for side in ('client', 'server'):
        blocks = jl(f'scratch/t50/out/profiles/table_{side}_extra_9.rows.jsonl')
        pay = pl[f'{side}/table_extra_9.dat']
        ck(len(blocks) == 251, f't50 extra_9 {side} 251 blocks')
        offs = [b['offset'] for b in blocks]
        ck(offs[0] == 12, f't50 extra_9 {side} first block @12 (after 12B header)')
        ck(all(offs[i] + blocks[i]['len'] == offs[i+1] for i in range(250)), f't50 extra_9 {side} blocks tile contiguously')
        mk = [b.get('marker') or {} for b in blocks]
        ck([m.get('ordinal') for m in mk] == list(range(251)), f't50 extra_9 {side} block ordinals 0..250')
        if side == 'server':
            ck(mk[0].get('name_ascii') == 'Les Fennecs' and mk[0].get('name_len') == 11, 'extra_9 server block0 == (0, 11, "Les Fennecs") raw')
            ok_bytes = pay[12:12+4] == b'\x00'*4 and struct.unpack_from('<I', pay, 16)[0] == 11 and pay[20:31] == b'Les Fennecs'
            ck(ok_bytes, 'extra_9 server raw bytes @12: ordinal0|len11|"Les Fennecs"')

    # 5. negatives preserved
    gd_s = json.dumps(gd) + json.dumps(prof)
    ck('362' in gd_s, 'server 362 wide-tiling negative recorded (row_id=0 variant)')
    ck('50331648' in gd_s or '50331648' in json.dumps(prof), 'client 6-tiling negative recorded (no-increase variant)')

    # 6. worker checks as subprocesses
    rb = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scripts/t50_nation_t9_profile.py'), '--selftest'],
                        capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    ck(rb.returncode == 0 and 'PASS' in (rb.stdout + rb.stderr).upper(), f'builder --selftest rc0 (rc={rb.returncode})')
    rv = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scratch/t50/out/verify.py'), '--check'],
                        capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    ck(rv.returncode == 0 and 'PASS' in (rv.stdout + rv.stderr).upper(), f't50 verify.py --check PASS rc0 (rc={rv.returncode})')
    ra = subprocess.run([sys.executable, '-I', '-B', str(ROOT/'scripts/t01_anchors.py')],
                        capture_output=True, text=True, env=ENV, cwd=str(ROOT))
    ck(ra.returncode == 0 and '7/7' in ra.stdout, f't01_anchors 7/7 (rc={ra.returncode})')

    print(f'\n=== t50 spot: {PASS}/{PASS+FAIL} ===')
    sys.exit(0 if FAIL == 0 else 1)

if __name__ == '__main__':
    main()
