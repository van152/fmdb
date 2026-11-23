"""t76c scratch: settle lcrg 5B item reference domain + weather UID density."""
import runpy, struct, json
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']
m = json.load(open('evidence/fm24/reports/editor_schema/master.json', encoding='utf-8'))

# weather UIDs from its own identity trailer
raw = load('client', 27)
pos, wid = 14, []
for j in range(334):
    ln = struct.unpack_from('<I', raw, pos)[0]
    end = pos + 4 + ln + 95 + 13
    wid.append(struct.unpack_from('<I', raw, end - 9)[0])
    pos = end
print('weather UIDs: n=%d min=%d max=%d dense0..333=%s distinct=%d'
      % (len(wid), min(wid), max(wid), sorted(wid) == list(range(334)), len(set(wid))))
print('  first 12:', wid[:12])

# language UIDs from language table (type? find)
print('\nlanguage table uid probe:')
for t in (10, 11, 12, 13, 14, 15, 16, 17):
    try:
        r = load('client', t)
        n = struct.unpack_from('<I', r, 8)[0]
        print('  t%-3d len=%-7d count=%d' % (t, len(r), n))
    except Exception as e:
        print('  t%-3d ERR %s' % (t, type(e).__name__))

# lcrg items both orderings
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
print('\nlcrg rows', len(rows), 'sum k', sum(k for _, k in rows))

for name, off, pt, rt in (('(pct u8, ref u32) @28+5i', 28, 0, 1),
                          ('(ref u32, pct u8) @28+5i', 28, 4, 0)):
    it = []
    for biz, k in rows:
        for i in range(k):
            o = off + 5 * i
            it.append((biz[o + pt], int.from_bytes(biz[o + rt:o + rt + 4], 'little')))
    p = [a for a, _ in it]
    r = [b for _, b in it]
    nn = [x for x in r if x != 0xFFFFFFFF]
    print(f'\n{name}: n={len(it)} pct<=100={sum(1 for x in p if x<=100)} pct_distinct={len(set(p))}')
    print(f'  ref null={len(r)-len(nn)} nonnull={len(nn)} distinct={len(set(nn))} '
          f'min={min(nn)} max={max(nn)}')
    for tgt, N in (('language', 126), ('nation', 251), ('weather', 334), ('city', 56293),
                   ('region', 28)):
        print(f'    ref < {tgt}({N}): {sum(1 for x in nn if x < N)}/{len(nn)}')
    print('  ref density 0..max:', len(set(nn)) / (max(nn) + 1))

print('\n=== item0 of every row (i=0)')
i0 = [(biz[28], int.from_bytes(biz[29:33], 'little')) for biz, k in rows if k >= 1]
print('  n=%d pct values=%s' % (len(i0), sorted({a for a, _ in i0})))
print('  ref values sample:', sorted({b for _, b in i0})[:20])

print('\n=== per-row: is item ref sequence sorted/increasing?')
inc = 0
for biz, k in rows:
    if k <= 1:
        inc += 1
        continue
    ok = all(int.from_bytes(biz[29 + 5 * i:33 + 5 * i], 'little')
             <= int.from_bytes(biz[34 + 5 * i:38 + 5 * i], 'little')
             for i in range(k - 1))
    inc += 1 if ok else 0
print('  monotone rows:', inc, '/', sum(1 for _, k in rows if k > 1))
