"""t76c scratch: FK lane tests for derby numeric region against live domains."""
import runpy, struct, sys, json
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']
NUM = {'client': 36, 'server': 42}
TEAM_N, CLUB_N, COMP_N, STAD_N, CITY_N, NATION_N = 84507, 84259, 7047, 48413, 56293, 251


def rows_derby(raw, num):
    pos, rows = 14, []
    for j in range(1567):
        p, names, nb = pos, [], 0
        for _ in range(4):
            ln = struct.unpack_from('<I', raw, p)[0]
            names.append(raw[p + 4:p + 4 + ln].decode('utf-8'))
            nb += ln
            p += 4 + ln
        end = pos + 16 + nb + num + 13
        rows.append(dict(row=j, start=pos, end=end, names=names,
                         num=raw[pos + 16 + nb:end - 13],
                         uid=struct.unpack_from('<III', raw, end - 13)[1]))
        pos = end
    return rows


for arch in ('client', 'server'):
    raw = load(arch, 18)
    rows = rows_derby(raw, NUM[arch])
    n = len(rows)
    print('=' * 24, arch, n)
    for off in (0, 4, 8, 12, 16, 20, 24, 28, 32):
        v = [int.from_bytes(r['num'][off:off + 4], 'little') for r in rows]
        live = [x for x in v if x != 0xFFFFFFFF]
        d = {'off': off, 'n': len(v), 'n_ff': v.count(0xFFFFFFFF),
             'n_zero': v.count(0),
             'min': min(live) if live else None, 'max': max(live) if live else None,
             'distinct': len(set(live))}
        for nm, lim in (('team84507', TEAM_N), ('club84259', CLUB_N),
                        ('comp7047', COMP_N), ('stad48413', STAD_N),
                        ('city56293', CITY_N), ('nation251', NATION_N)):
            d[nm] = round(sum(1 for x in live if x < lim) / max(1, len(live)), 4)
        print(' ', json.dumps(d))
    # identity: Dtm1 != Dtm2 ?
    a = [int.from_bytes(r['num'][4:8], 'little') for r in rows]
    b = [int.from_bytes(r['num'][8:12], 'little') for r in rows]
    print('  Dtm1!=Dtm2:', sum(1 for x, y in zip(a, b) if x != y), '/', n)
    print('  Dtm1 in [0,club):', sum(1 for x in a if x < CLUB_N), 'Dtm2:', sum(1 for y in b if y < TEAM_N))
    print('  sorted-pair check (Dtm1<Dtm2):', sum(1 for x, y in zip(a, b) if x < y), '/', n)
    print('  Dtm values look like UIDs (>1e6):', sum(1 for x in a if x > 1_000_000))
    print('  sample Dtm pairs:', list(zip(a[:6], b[:6])), 'names', rows[0]['names'])
    # u16 pieces
    print('  u16@0 (day) range', min(int.from_bytes(r['num'][0:2], 'little') for r in rows),
          max(int.from_bytes(r['num'][0:2], 'little') for r in rows))
    print('  u16@2 (year) range', min(int.from_bytes(r['num'][2:4], 'little') for r in rows),
          max(int.from_bytes(r['num'][2:4], 'little') for r in rows))
    print('  b34 max', max(r['num'][34] for r in rows), 'b35 max', max(r['num'][35] for r in rows))
    if arch == 'server':
        print('  server extra 6B at 28..33:', Counter(r['num'][28:34].hex() for r in rows).most_common(3))
