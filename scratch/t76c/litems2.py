"""t76c scratch: lcrg item block starts at 23 with k+1 items (leading pct==0)."""
import runpy, struct
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']
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
print('rows', len(rows), 'k sum', sum(k for _, k in rows))

print('\n=== prefix 0..22 fixed bytes check')
for off in range(23):
    v = [b[off] for b, _ in rows]
    print(f'  b{off:2} d={len(set(v)):3} [{min(v):3},{max(v):3}] z={v.count(0):4}')

print('\n=== items at 23 + 5i, i in 0..k  (k+1 items)')
ok = all(len(b) == 23 + 5 * (k + 1) for b, k in rows)
print('  23 + 5*(k+1) == biz_len for all rows:', ok)

it = []
for b, k in rows:
    for i in range(k + 1):
        o = 23 + 5 * i
        it.append((i, b[o], int.from_bytes(b[o + 1:o + 5], 'little')))
print('  total items:', len(it))
lead = [x for x in it if x[0] == 0]
body = [x for x in it if x[0] > 0]
print('  leading items (i=0): n=%d pct=%s ref=[%d,%d] distinct=%d'
      % (len(lead), sorted({p for _, p, _ in lead}),
         min(r for *_, r in lead), max(r for *_, r in lead),
         len({r for *_, r in lead})))
print('  body items: n=%d pct=%s' % (len(body), sorted({p for _, p, _ in body})))
nn = [r for _, _, r in body if r != 0xFFFFFFFF]
print('  body ref: null=%d nonnull=%d distinct=%d [%d,%d]'
      % (len(body) - len(nn), len(nn), len(set(nn)), min(nn), max(nn)))
for tgt, N in (('language', 126), ('nation', 251), ('weather', 334), ('region', 28)):
    print(f'    < {tgt}({N}): {sum(1 for x in nn if x < N)}/{len(nn)}')
print('  body ref density over 0..max:', len(set(nn)) / (max(nn) + 1))

print('\n=== leading item ref: is it a small dense ordinal?')
lr = [r for *_, r in lead]
print('  distinct:', len(set(lr)), 'values:', sorted(set(lr))[:25])
print('  == row index j?', sum(1 for (b, k), (i, p, r) in
                               zip(rows, lead) if r == 0))

print('\n=== body ref: same as leading ref of the same row?')
same = 0
for b, k in rows:
    lr0 = int.from_bytes(b[24:28], 'little')
    for i in range(1, k + 1):
        if int.from_bytes(b[23 + 5 * i + 1:23 + 5 * i + 5], 'little') == lr0:
            same += 1
print('  body item equal to row leading ref:', same)
