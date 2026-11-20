"""t76c scratch: structural partition search (sum-to-100 blocks) for weather mid region."""
import runpy, struct, sys
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']


def rows_weather(raw):
    pos, rows = 14, []
    for j in range(334):
        ln = struct.unpack_from('<I', raw, pos)[0]
        end = pos + 4 + ln + 95 + 13
        rows.append(dict(row=j, start=pos, namelen=ln, end=end,
                         name=raw[pos + 4:pos + 4 + ln].decode('utf-8'),
                         mid=raw[pos + 4 + ln:end - 13]))
        pos = end
    return rows


raw = load('client', 27)
rows = rows_weather(raw)
M = [r['mid'] for r in rows]
n = len(M)
print('rows', n, 'mid len', len(M[0]))

print('\n=== runs of length L whose sum == 100 for all rows (u8)')
for L in (5, 10):
    hits = []
    for a in range(0, 95 - L + 1):
        s = {sum(m[a:a + L]) for m in M}
        if s == {100}:
            hits.append(a)
    print(f'  L={L} exact-sum-100 starts:', hits)

print('\n=== candidates: sum==100 for >=95% rows')
for L in (5, 10):
    hits = []
    for a in range(0, 95 - L + 1):
        c = sum(1 for m in M if sum(m[a:a + L]) == 100)
        if c >= 0.95 * n:
            hits.append((a, round(c / n, 3)))
    print(f'  L={L}:', hits)

print('\n=== all-byte columns with max<=100 exclusive of const')
cols = {}
for a in range(95):
    v = [m[a] for m in M]
    if 1 <= max(v) <= 100:
        cols[a] = (len(set(v)), min(v), max(v))
print('  offsets with 0<=val<=100:', {k: v for k, v in cols.items()})
