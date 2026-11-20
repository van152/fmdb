"""t76c scratch: determine weather 23B block field offsets + lcrg item uid set membership."""
import runpy, struct, sys, json
from collections import Counter
from pathlib import Path

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']


def rows_weather(raw):
    pos, rows = 14, []
    for j in range(334):
        ln = struct.unpack_from('<I', raw, pos)[0]
        end = pos + 4 + ln + 95 + 13
        rows.append(dict(row=j, namelen=ln, mid=raw[pos + 4 + ln:end - 13],
                         name=raw[pos + 4:pos + 4 + ln].decode('utf-8')))
        pos = end
    return rows


raw = load('client', 27)
W = rows_weather(raw)
M = [r['mid'] for r in W]
n = len(M)

print('=== window sum==100 scan inside block base 3+23b, L=5..12')
for b in range(4):
    base = 3 + 23 * b
    hits = []
    for L in range(5, 13):
        for r in range(base, base + 23 - L + 1):
            c = sum(1 for m in M if sum(m[r:r + L]) == 100)
            if c >= 0.93 * n:
                hits.append((L, r - base, round(c / n, 3)))
    print(f'  block{b} base={base}:', hits)

print('\n=== block 3 (base 72) layout details, and block0 for contrast')
for b in range(4):
    base = 3 + 23 * b
    print(f'-- block{b} base={base}')
    for r in range(23):
        v = [m[base + r] for m in M]
        print(f'   rel{r:2} abs{base + r:3} min={min(v):3} max={max(v):3} '
              f'd={len(set(v)):3} zero={v.count(0):4} top={Counter(v).most_common(2)}')

print('\n=== per-block "sd" candidate: rel0 monotone? rel0 vs rel1 relation')
for b in range(4):
    base = 3 + 23 * b
    v0 = [m[base] for m in M]
    v1 = [m[base + 1] for m in M]
    print(f'  block{b}: rel0 {min(v0)}..{max(v0)} rel1 {Counter(v1).most_common(3)}')
print('\n=== does block3 rel0 look like start-day with wrap? first 12 rows:')
for b in range(4):
    print('  block', b, [m[3 + 23 * b] for m in M[:12]])
