"""t76c scratch: weather period-23 block structure test."""
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

print('=== period check: are mid[3+b*23 + r] distributions equal across b?')
for r in range(23):
    cols = [[m[3 + 23 * b + r] for m in M] for b in range(4)]
    same = all(cols[0] == c for c in cols[1:])
    print(f' rel{r:2}: same={same} distinct={[len(set(c)) for c in cols]} '
          f'max={[max(c) for c in cols]}')

print('\n=== within block b=0 (base 3): search sums==100 runs')
for L in (5, 8):
    for a in range(3, 26 - L + 1):
        s = {sum(m[a:a + L]) for m in M}
        if s == {100}:
            print(f'  L={L} start={a} rel={a - 3} EXACT 100')
        else:
            c = sum(1 for m in M if sum(m[a:a + L]) == 100)
            if c > 0.9 * n:
                print(f'  L={L} start={a} rel={a - 3} rate={c / n:.3f}')

print('\n=== candidate field block per schema: 1 + 5 + 5 + 8 + 1 = 20 (u8 each)')
# hypothesis: rel0 day, rel1-5 precip(5), rel6-10 wind(5), rel11-18 temp(8), rel19 dn
for rel_base, names in (
        (0, ['day', 'p0', 'p1', 'p2', 'p3', 'p4', 'w0', 'w1', 'w2', 'w3', 'w4',
             'te', 'tv', 't0', 't1', 't2', 't3', 't4', 't5', 't6', 't7', 'dn']),):
    pass

print('\n=== sum checks for schema-aligned guesses (block base 3)')
def sums(a, L):
    return [sum(m[a:a + L]) for m in M]
for a, L, tag in ((4, 5, 'p@4'), (9, 5, 'p@9'), (5, 5, 'p@5'),
                  (10, 5, 'w@10'), (9, 5, 'x'), (15, 5, 'x15'),
                  (16, 8, 't@16'), (15, 8, 't@15'), (12, 8, 't@12')):
    s = sums(a, L)
    print(f'  {tag} L={L}: exact100={sum(1 for x in s if x == 100)}/{n} '
          f'min={min(s)} max={max(s)}')

print('\n=== 4-byte grouping at 3+b*23: u32 spans')
for a in (3, 4):
    for L in (20, 23):
        pass
print('bytes 0..2 const:', [Counter(m[i] for m in M).most_common(2) for i in range(3)])
print('byte3:', Counter(m[3] for m in M).most_common(6), 'max', max(m[3] for m in M))
print('byte4:', Counter(m[4] for m in M).most_common(4))
