"""t76c scratch: lcrg alignment — test the 5k tail as (u32 uid, u8 pct) items."""
import runpy, struct, sys
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']


def rows_lcrg(raw):
    pos, rows = 14, []
    for j in range(2488):
        for k in range(200):
            ln = 41 + 5 * k
            end = pos + ln
            o, a, b = struct.unpack_from('<III', raw, end - 13)
            if o == j and a == b != 0 and raw[end - 1] == 0:
                rows.append(dict(row=j, start=pos, end=end, ln=ln, k=k,
                                 biz=raw[pos:end - 13]))
                pos = end
                break
    return rows


raw = load('client', 47)
rows = rows_lcrg(raw)
print('rows', len(rows))

# 1. offset 22 vs k
m22 = sum(1 for r in rows if r['biz'][22] == r['k'])
print('biz[22]==k:', m22, '/', len(rows))
bad = [(r['row'], r['k'], r['biz'][22], r['biz'].hex()) for r in rows if r['biz'][22] != r['k']][:5]
print('mismatches', bad)

# 2. tail = last 5k bytes? then prefix = 28 bytes fixed. Inspect tail items.
def tail_items(r):
    t = r['biz'][28:]
    if len(t) != 5 * r['k']:
        return None
    return [(struct.unpack_from('<I', t, i * 5)[0], t[i * 5 + 4]) for i in range(r['k'])]

ok = sum(1 for r in rows if tail_items(r) is not None)
print('tail-at-28 length ok:', ok, '/', len(rows))
for r in rows:
    if r['k'] >= 3:
        print('row', r['row'], 'k', r['k'], 'prefix', r['biz'][:28].hex(' '),
              'tail', tail_items(r))
        if r['k'] >= 6:
            break
# distribution of tail uids and pcts
uids = Counter()
pcts = Counter()
for r in rows:
    t = tail_items(r)
    if t:
        for u, p in t:
            uids[u] += 1
            pcts[p] += 1
print('\ntail uid top20', uids.most_common(20))
print('tail pct distinct', len(pcts), 'top', pcts.most_common(12))
print('tail uid max', max(uids))
