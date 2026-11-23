"""t76c scratch: lcrg tail-item alignment hypotheses vs city/nation/weather domains."""
import runpy, struct, sys
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']

CITY_N = 56293
NATION_N = 251
WEATHER_N = 334


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

def rate(vals, n):
    return sum(1 for v in vals if v < n) / max(1, len(vals))

print('=== hypothesis A: groups of 5 from idx23 as (u32 uid, u8 pct), count k+1')
uA, pA, tailA = [], [], []
for r in rows:
    b = r['biz'][23:]
    assert len(b) == 5 * (r['k'] + 1), (r['row'], len(b), r['k'])
    for i in range(0, len(b), 5):
        u = int.from_bytes(b[i:i + 4], 'little')
        p = b[i + 4]
        uA.append(u); pA.append(p)
print(' u32 <city', rate(uA, CITY_N), '<nation', rate(uA, NATION_N),
      '<weather', rate(uA, WEATHER_N), 'n', len(uA), 'null', uA.count(0xFFFFFFFF))
print(' pct<=100', rate(pA, 101), 'top', Counter(pA).most_common(6))

print('=== hypothesis B: groups of 5 from idx23 as (u8 pct, u32 uid)')
uB, pB = [], []
for r in rows:
    b = r['biz'][23:]
    for i in range(0, len(b), 5):
        p = b[i]; u = int.from_bytes(b[i + 1:i + 5], 'little')
        uB.append(u); pB.append(p)
print(' u32 <city', rate(uB, CITY_N), '<nation', rate(uB, NATION_N),
      '<weather', rate(uB, WEATHER_N), 'n', len(uB), 'null', uB.count(0xFFFFFFFF))
print(' pct<=100', rate(pB, 101), 'top', Counter(pB).most_common(6))

print('=== hypothesis C: prefix 28 fixed, then k items of 5 (u32 uid, u8 pct)')
uC, pC = [], []
for r in rows:
    b = r['biz'][28:]
    assert len(b) == 5 * r['k']
    for i in range(0, len(b), 5):
        uC.append(int.from_bytes(b[i:i + 4], 'little')); pC.append(b[i + 4])
print(' u32 <city', rate(uC, CITY_N), 'null', uC.count(0xFFFFFFFF), 'n', len(uC))

print('=== per-offset invariant checks')
print(' u8@22 == k all:', all(r['biz'][22] == r['k'] for r in rows))
print(' u8@1,2,3 zero all:', all(r['biz'][1:4] == b'\0\0\0' for r in rows))
print(' u8@20 zero all:', all(r['biz'][20] == 0 for r in rows))
print(' u8@21 in {0,1}:', Counter(r['biz'][21] for r in rows))
print(' u8@0 <251 rate:', rate([r['biz'][0] for r in rows], 251),
      'distinct', len({r['biz'][0] for r in rows}))
print(' u32@4 <1e9 rate:', rate([int.from_bytes(r["biz"][4:8], "little") for r in rows], 10**9))
print(' u32@4 zeros:', sum(1 for r in rows if int.from_bytes(r["biz"][4:8], "little") == 0))
print(' sum u8@8..11 <=100 rate:',
      sum(1 for r in rows if sum(r['biz'][8:12]) <= 100) / len(rows))
print(' u8@8..11 max each:', [max(r['biz'][8 + i] for r in rows) for i in range(4)])
print(' u8@12..19 max each:', [max(r['biz'][12 + i] for r in rows) for i in range(8)])
print(' u32@16 max', max(int.from_bytes(r['biz'][16:20], 'little') for r in rows))
print(' u16@20 values', Counter(int.from_bytes(r['biz'][20:22], 'little') for r in rows).most_common(8))
