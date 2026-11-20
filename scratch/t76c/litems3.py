"""t76c scratch: lcrg item reference — decide ordinal target vs per-row index."""
import runpy, struct
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']

# find the language table: scan type ids for a ~126-row table
print('=== table census (type id -> rows) to locate language/nation')
census = {}
for t in range(1, 120):
    try:
        r = load('client', t)
        census[t] = struct.unpack_from('<I', r, 8)[0]
    except Exception:
        pass
small = {t: n for t, n in census.items() if n <= 400}
print('  small tables:', sorted(small.items(), key=lambda x: x[1]))

raw = load('client', 47)
rows, pos = [], 14
for j in range(2488):
    for k in range(200):
        ln = 41 + 5 * k
        end = pos + ln
        o, a, b = struct.unpack_from('<III', raw, end - 13)
        if o == j and a == b != 0 and raw[end - 1] == 0:
            rows.append((raw[pos:end - 13], k))
            pos = end
            break

print('\n=== items at 28+5i (i in 0..k-1): uniqueness / range within row')
uniq = inrange = tot = 0
for b, k in rows:
    refs = [int.from_bytes(b[29 + 5 * i:33 + 5 * i], 'little') for i in range(k)]
    live = [r for r in refs if r != 0xFFFFFFFF]
    tot += 1
    uniq += 1 if len(set(live)) == len(live) else 0
    inrange += 1 if all(r < k for r in live) else 0
print(f'  rows with k>0: {sum(1 for _,k in rows if k)}  refs-unique-within-row: {uniq}')
print(f'  rows where all refs < k (per-row index): {inrange}')

print('\n=== ref value histogram (top 20) + null share')
allref = []
for b, k in rows:
    allref += [int.from_bytes(b[29 + 5 * i:33 + 5 * i], 'little') for i in range(k)]
nn = [r for r in allref if r != 0xFFFFFFFF]
print('  null', len(allref) - len(nn), 'nonnull', len(nn), 'distinct', len(set(nn)))
print('  top:', Counter(nn).most_common(12))

print('\n=== pct distribution (should be 0..100)')
allpct = []
for b, k in rows:
    allpct += [b[28 + 5 * i] for i in range(k)]
print('  n', len(allpct), 'min', min(allpct), 'max', max(allpct),
      'distinct', len(set(allpct)), 'sum-range', (min(allpct), max(allpct)))
print('  top:', Counter(allpct).most_common(12))

print('\n=== per-row pct sum (should be ~100 if percentages)')
s = [sum(b[28 + 5 * i] for i in range(k)) for b, k in rows if k]
print('  sum==100:', s.count(100), '/', len(s), '  hist:',
      Counter(s).most_common(8))

print('\n=== b24..27 (nullable u32) vs refs of the same row')
eq = 0
for b, k in rows:
    v = int.from_bytes(b[24:28], 'little')
    if v != 0xFFFFFFFF and k and v == int.from_bytes(b[29:33], 'little'):
        eq += 1
print('  b24 == first item ref:', eq)
v24 = [int.from_bytes(b[24:28], 'little') for b, _ in rows]
n24 = [x for x in v24 if x != 0xFFFFFFFF]
print('  b24 nonnull', len(n24), 'distinct', len(set(n24)), 'max', max(n24))
print('  b24 values sample:', sorted(set(n24))[:15])
