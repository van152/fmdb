#!/usr/bin/env python3
"""Commander independent spot for t46 nation server table_10 data-side profile (L1/L2).
Does NOT import builder/verify/fm24_dump/t38. Recomputes closure/identity from payload,
cross-matches server row IDs against client t25 witnesses rebuilt from client payload.
"""
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import sys

ROOT = Path('D:/tmp2b/fm24-db')
DATA = Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
OUT = ROOT/'scratch/t46/out'
CODEC = ROOT.parent/'fm24/scripts/modding_read_dbdat.py'
PASS = FAIL = 0

def ck(ok, msg):
    global PASS, FAIL
    if ok: PASS += 1; print(f'[PASS] {msg}')
    else: FAIL += 1; print(f'[FAIL] {msg}')

def H(b): return sha256(b).hexdigest()
def U(b, i): return int.from_bytes(b[i:i+4], 'little')

def payload(side, tid):
    codec = runpy.run_path(str(CODEC))
    _, blob, d = codec['_entries'](DATA/f'{side}_db.dat')
    base = d['data_base']
    ents = {e['path']: e for e in d['entries']}
    e = ents[f'{side}_db/table_{tid}.dat']
    a = base + e['offset']; b = a + e['packed_size']
    import zstandard as z
    raw = z.ZstdDecompressor().decompress(blob[a:b], max_output_size=e['size'], allow_extra_data=False)
    assert len(raw) == e['size']
    return raw, len(ents), base

def main():
    srv, sn, sb = payload('server', 10)
    cli, cn, cb = payload('client', 10)
    ck(sn == 77 and sb == 34 and cn == 31 and cb == 34, 'directories server77/client31 data_base34')
    ck(len(srv) == 422345 and H(srv) == '19337841e40d012863cb3aeca72141ec3b059419b8d87e54a6f380e8974b047f', 'server table_10 422345B SHA 19337841')
    ck(len(cli) == 24732 and H(cli) == '7e9d740b9ee6900965d8616a136ea4bc54a0f7207f9727eac72badfb727f6c34', 'client table_10 24732B SHA 7e9d740b (matches t25)')

    rows = [json.loads(l) for l in (OUT/'profiles/table_server_10.rows.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()]
    ck(len(rows) == 251, 'server 251 rows')
    lens = [r['len'] for r in rows]
    ck(sum(lens) == 422323, 'sum row_lens 422323')
    ck(14 + sum(lens) + 8 == 422345 == len(srv), 'closure 14 + 422323 + 8 = 422345')
    # contiguous offsets + raw matches payload
    pos = 14; ok_off = ok_raw = True
    for r in rows:
        if r['offset'] != pos: ok_off = False
        if bytes.fromhex(r['raw_hex']) != srv[r['offset']:r['offset']+r['len']]: ok_raw = False
        pos += r['len']
    ck(ok_off, 'row offsets contiguous from 14')
    ck(ok_raw, 'every row raw_hex == payload slice')
    ck(pos == len(srv) - 8, 'rows end at payload-8 (footer)')
    block = b''.join(srv[r['offset']:r['offset']+r['len']] for r in rows)
    ck(H(block) == '4162770e55007a453c8ac55381458d28b414a0b5ba3836d6365a0887558ea45b', 'row-block SHA 4162770e')
    ck(len(set(lens)) == 195 and min(lens) == 141 and max(lens) == 30993, '195 distinct lengths, span 141..30993')

    # server identity tails: ordinal|id|id|00 at row_end-13
    sids = {}; ok_tail = True; ords = []
    for r in rows:
        e = r['offset'] + r['len']
        t = e - 13
        o, i1, i2, mk = U(srv, t), U(srv, t+4), U(srv, t+8), srv[t+12]
        ident = r['identity']
        if not (i1 == i2 and mk == 0 and ident['ordinal'] == o and ident['row_id'] == i1 and ident['tail_offset_in_row'] == r['len']-13):
            ok_tail = False
        sids[o] = i1; ords.append(o)
    ck(ok_tail, 'all 251 identity tails ordinal|id|id|00 at row_end-13 match rows.jsonl')
    ck(sorted(ords) == list(range(251)) and len(set(sids.values())) == 251, 'server ordinals 0..250, row IDs unique')

    # L2: rebuild client witnesses from client payload using t25 framing
    t25 = json.loads((ROOT/'scratch/t25/out/cursor_nation.json').read_bytes())
    ck(t25['row_count'] == 251 and t25['closure_equation'] == '14 + 24710 + 8 = 24732', 't25 client 251 rows closure 24732')
    cids = {}; ok_c = True
    for cr in t25['rows']:
        e = cr['row_start_payload'] + cr['row_span']
        t = e - 13
        o, i1, i2, mk = U(cli, t), U(cli, t+4), U(cli, t+8), cli[t+12]
        if not (i1 == i2 and mk == 0): ok_c = False
        cids[o] = i1
    ck(ok_c and len(cids) == 251, 'client t25 identity tails rebuilt from payload (251)')
    ck(sids == cids, 'L2 server ordinal->row_id set == client t25 witness set (251/251)')

    # grammar differential
    g = json.loads((OUT/'grammar_diff_client_server.json').read_bytes())
    og = g['overall_row_grammar']
    ck(og['status'] == 'different' and og['client_first_row_span'] == 65 and og['server_first_row_span'] == 632, 'grammar different: client row0 65B vs server 632B')
    ck(rows[0]['len'] == 632, 'server row0 span 632 confirmed')
    seg = g['segments']
    ck(all(seg[s]['server']['count_location'] is None for s in 'ABCD'), 'A/B/C/D server count locations unknown (no overclaim)')
    pa = seg['A']['same_offset_probe']
    ck(pa['offset'] == 24 and pa['interpreted_with_client_width_as_signed'] == -90 and pa['client_first_row_count_at_that_slot'] == 3 and pa['matches'] is False, 'A probe +24 server -90 vs client 3 (falsification only)')
    ck(g['identity_tail']['rows_matched'] == 251 and g['status'] == 'partial_server_internal_segments_unresolved', 'identity tail 251 matched; status partial unresolved')

    # no L3/L4 overclaim
    prof = json.loads((OUT/'profiles/table_server_10.profile.json').read_bytes())
    txt = json.dumps(prof) + json.dumps(g)
    ck('"L3"' not in txt or prof.get('new_L3_claims', 0) == 0, 'no L3 field assignments in profile')
    ck(g.get('L4', 0) == 0 and prof.get('L4', 0) == 0, 'L4 = 0')

    print(f'\n=== t46 spot: {PASS}/{PASS+FAIL} ===')
    return 0 if FAIL == 0 else 1

if __name__ == '__main__':
    sys.exit(main())