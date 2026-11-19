#!/usr/bin/env python3
"""Commander independent spot-check for t44 Cafl/Cvfl club_links.dat.
Does NOT import builder, verify.py, fm24_dump, t38 or ReaderCFG.
Re-derives club ordinal->identity domain from client table_3 with its own walk.
"""
import calendar
from collections import Counter
from hashlib import sha256
import json
import os
from pathlib import Path
import runpy
import struct as S
import sys

ROOT = Path('D:/tmp2b/fm24-db')
DATA = Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
OUT = ROOT/'scratch/t44/out'
CODEC = ROOT.parent/'fm24/scripts/modding_read_dbdat.py'
HDR = bytes.fromhex('03017461642ef10d')
PASS = FAIL = 0

def ck(ok, msg):
    global PASS, FAIL
    if ok:
        PASS += 1; print(f'[PASS] {msg}')
    else:
        FAIL += 1; print(f'[FAIL] {msg}')

def H(b): return sha256(b).hexdigest()
def U(b, i): return int.from_bytes(b[i:i+4], 'little')
def I8(b, i): return int.from_bytes(b[i:i+1], 'little', signed=True)

def load_member(side, name):
    codec = runpy.run_path(str(CODEC))
    _, blob, d = codec['_entries'](DATA/f'{side}_db.dat')
    base = d['data_base']
    ents = {e['path']: e for e in d['entries']}
    if name not in ents:
        return None, None, base, len(ents)
    import zstandard as z
    e = ents[name]
    a = base + e['offset']
    b = a + e['packed_size']
    bound = min((base+v['offset'] for v in ents.values() if v['offset'] > e['offset']), default=d['toc_offset'])
    part = blob[a:b]
    assert part[:4] == bytes.fromhex('28b52ffd') and b <= bound
    raw = z.ZstdDecompressor().decompress(part, max_output_size=e['size'], allow_extra_data=False)
    assert len(raw) == e['size']
    return raw, dict(start=a, end=b, bound=bound, packed_sha=H(part), payload_sha=H(raw), size=e['size']), base, len(ents)

def club_domain():
    """Independent ordinal->identity walk over client table_3 (variable rows, 2 strings + triple)."""
    b, _, _, _ = load_member('client', 'client_db/table_3.dat')
    s, _, _, _ = load_member('server', 'server_db/table_3.dat')
    n = U(b, 8)
    assert b[:8] == HDR == s[:8] and n == U(s, 8)
    p = 14; mapping = {}
    for j in range(n):
        tag = S.pack('<I', j)
        hits = []
        q = b.find(tag, p+20, min(p+8192, len(b)-12))
        while q >= 0:
            x, y = U(b, q+4), U(b, q+8)
            if x == y and b[q+12] in (0, 12):
                hits.append((q, x))
            q = b.find(tag, q+1, min(p+8192, len(b)-12))
        def text_end(a):
            for _ in range(2):
                sz = U(b, a)
                if sz > 200: return -1
                try: b[a+4:a+4+sz].decode('utf-8')
                except UnicodeError: return -1
                a += 4+sz
            return a+3
        ends = {text_end(p+25), text_end(p+26)}
        shaped = [h for h in hits if h[0] in ends]
        hits = shaped if shaped else [h for h in hits if h[0] < p+8192]
        assert len(hits) == 1, f'club triple {j}: {hits[:4]}'
        (q, x), = hits
        mapping[j] = x; p = q+13
    assert p+8 == len(b) and len(set(mapping.values())) == n
    # confirm ordered triple sequence on server too
    triples = [S.pack('<III', i, x, x) for i, x in mapping.items()]
    p = 13
    for t in triples:
        q = s.find(t, p, len(s)-9); assert q >= 0; p = q+12
    assert p == len(s)-9
    return mapping, n

def main():
    f = json.loads((OUT/'fields_cafl_cvfl.json').read_bytes())
    c = json.loads((OUT/'cursor_club_links.json').read_bytes())
    raw, meta, base, nent = load_member('server', 'server_db/club_links.dat')
    ck(nent == 77 and base == 34, 'server directory 77 entries data_base 34')
    ck(meta['start'] == 38906250 and meta['end'] == meta['bound'] == 38970194, 'member bounds [38906250,38970194)')
    ck(meta['size'] == 435279 and len(raw) == 435279, 'payload size 435279')
    ck(meta['payload_sha'] == '8933328064b13a9d8dc153dd5b455970a7c28ada1e24f4ecc9df35735f42f3d2', 'payload SHA 8933328064')
    ck(meta['packed_sha'] == '894f1efb9caf18482402198ed19294d04725a583ca262a6a01b2ed95c2222fe0', 'packed-region SHA 894f1efb (not payload)')
    cl, _, _, cn = load_member('client', 'client_db/club_links.dat')
    ck(cl is None and cn == 31, 'client club_links absent (31 entries), not empty')

    ck(raw[:8] == HDR and U(raw, 8) == 9261, 'header 8B + count@8 == 9261')
    ck(12 + 9261*47 == 435279, 'closure 12 + 9261*47 + 0 = 435279')
    rb = H(raw[12:12+9261*47])
    ck(rb == c['replay']['row_block_sha256'] == '17a167f0bb5945c19eacaf3a7884ea3c14b29eb4185aaf533e57f9a7ce89e75c', 'row-block SHA 17a167f0')

    # independent club domain
    mapping, nclub = club_domain()
    uid = set(mapping.values())
    ck(nclub == 84259 == c['target_club_domain']['actual_ordinals'], 'club domain 84259 actual ordinals')
    ck(H(b''.join(S.pack('<III', i, x, x) for i, x in mapping.items())) == c['target_club_domain']['key_map_sha256'], 'key-map SHA 42c81780')

    # walk rows
    A = []; B = []; typ = []; yfee = []; fri = []; msls = []; pwgp = []; stdt = []; endt = []; words = []
    for j in range(9261):
        o = 12 + 47*j
        A.append(U(raw, o+0)); B.append(U(raw, o+9))
        typ.append(I8(raw, o+4)); words.append(U(raw, o+5))
        stdt.append(U(raw, o+13)); endt.append(U(raw, o+17))
        yfee.append(int.from_bytes(raw[o+25:o+29], 'little', signed=True))
        fri.append(I8(raw, o+35)); msls.append(I8(raw, o+36)); pwgp.append(I8(raw, o+42))

    ep = f['endpoint_profiles']
    ck(all(v in mapping for v in A) and ep['A']['actual_ordinal_hits'] == 9261, 'affl A 9261/9261 ordinal hits')
    ck(all(v in mapping for v in B) and ep['B']['actual_ordinal_hits'] == 9261, 'affl B 9261/9261 ordinal hits')
    ck(len(set(A)) == ep['A']['distinct_ordinals'] == 3814, 'affl A distinct 3814')
    ck(len(set(B)) == ep['B']['distinct_ordinals'] == 7534, 'affl B distinct 7534')
    ck(sum(v not in uid for v in A) == ep['A']['wrong_uid_row_misses'] == 5751, 'affl A wrong-UID row misses 5751')
    ck(sum(v not in uid for v in B) == ep['B']['wrong_uid_row_misses'] == 8560, 'affl B wrong-UID row misses 8560')
    ck(A[0] == 1270 and mapping[A[0]] == 1688 and ep['A']['first']['target_identity'] == 1688, 'row0 A=1270 -> identity 1688')
    ck(B[0] == 11272 and mapping[B[0]] == 4212156 and ep['B']['first']['target_identity'] == 4212156, 'row0 B=11272 -> identity 4212156')
    ck(all(a != b for a, b in zip(A, B)), 'no self-link A==B in archive')

    # type held: enum missing 21, 609 raw
    tc = Counter(typ)
    ck(tc.get(21, 0) == 609, 'type=21 count 609 (held_domain_conflict)')
    ck(typ[12] == 21 and 12+47*12+4 == 580, 'type first counterexample row12 @580 = 21')
    # yfee held: 8984 -1
    ck(sum(v == -1 for v in yfee) == 8984, 'yfee -1 count 8984 (held)')
    ck(raw[12+25:12+29] == bytes.fromhex('ffffffff'), 'yfee row0 @37 = ffffffff')
    # fri%/pwgp L3
    ck(sum(v == -1 for v in fri) == 7715, 'fri% -1 count 7715')
    ck(all(0 <= v <= 100 for v in fri if v != -1), 'fri% live in [0,100]')
    ck(sum(v == -1 for v in pwgp) == 131, 'pwgp -1 count 131')
    ck(sum(v == 0 for v in pwgp) == 8776, 'pwgp raw0 count 8776 (not -1)')
    ck(all(0 <= v <= 100 for v in pwgp if v != -1), 'pwgp live in [0,100]')
    # msls held all -1
    ck(all(v == -1 for v in msls) and raw[12+36] == 0xff, 'msls all -1 (held_all_missing), row0 @48 ff')

    # dates
    def yr(v): return v >> 16
    def day(v): return v & 0x1ff
    def valid(v):
        y, d = yr(v), day(v)
        return 1900 <= y <= 2100 and 1 <= d <= (366 if calendar.isleap(y) else 365)
    ck(all(valid(v) for v in stdt) and all(valid(v) for v in endt), 'stdt/endt packed date day/year valid (leap-aware)')
    ck(min(map(yr, stdt)) == 1900 and max(map(yr, stdt)) == 2024, 'stdt year 1900..2024')
    ck(min(map(yr, endt)) == 1900 and max(map(yr, endt)) == 2042, 'endt year 1900..2042')
    ck(sum(v == (1900 << 16 | 1) for v in stdt) == 6909, 'stdt default 1900day1 count 6909')
    ck(sum(v == (1900 << 16 | 1) for v in endt) == 8902, 'endt default 1900day1 count 8902')

    # bitmap: 20 masks share u32 @row+5
    BITS = dict(frly=1, golo=2, fotb=3, plfr=4, yutr=5, perm=6, smbo=7, fnhl=9, hlwf=10, mrrl=13,
                scks=14, cpsd=15, ualf=16, lpfs=17, ustf=18, yout=19, rsrv=20, pfpr=21, UsSK=23, bttr=28)
    fc = f['flag_counts']
    ck(len(fc) == 32, 'flag_counts 32-element word-bit histogram')
    okbits = True
    for code, bit in BITS.items():
        setn = sum((w >> bit) & 1 for w in words)
        if setn != fc[bit]:
            okbits = False; print(f'  bit {code}({bit}) set {setn} != flag_counts {fc[bit]}')
    ck(okbits, 'all 20 named bit set-counts match flag_counts')
    ck(words[0] == 0x048001e2 and (words[0] >> 1) & 1 == 1 and (words[0] >> 2) & 1 == 0, 'row0 word e2018004: frly set, golo clear')
    # cross-check occurrence counts for frly
    fr = [o for o in f['occurrences']['Cafl'] if o['code'] == 'frly'][0]
    ck(fr['bit_index'] == 1 and fr['counts'] == {'0': 7292, '1': 1969} and fr['row_offset'] == 5, 'frly occurrence bit1 row5 counts{0:7292,1:1969}')

    # grades
    g = f['occurrence_grades']
    ck(g['Cafl'] == {'L3': 26, 'held_all_missing': 1, 'held_domain_conflict': 2}, 'Cafl grades 26 L3 + 1 all_missing + 2 domain_conflict')
    ck(g['Cvfl'] == {'L3': 16, 'held_domain_conflict': 2, 'runtime_only_no_wire_slot': 1}, 'Cvfl grades 16 L3 + 2 domain_conflict + 1 runtime_only')
    ck(len(f['occurrences']['Cafl']) == 29 and len(f['occurrences']['Cvfl']) == 19, 'Cafl 29 / Cvfl 19 scoped occurrences')
    ck(f['L4'] == 0, 'L4 = 0')

    # t35 negative preserved verbatim
    t35 = ROOT/'scratch/t35/out/cafl_cvfl_discovery.json'
    ck(H(t35.read_bytes()).startswith('35a7553f'), 't35 negative JSON SHA 35a7553f unchanged')

    print(f'\n=== t44 spot: {PASS}/{PASS+FAIL} ===')
    return 0 if FAIL == 0 else 1

if __name__ == '__main__':
    sys.exit(main())