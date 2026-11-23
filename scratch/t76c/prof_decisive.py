"""t76c scratch: decisive block-structure tests for weather(27) and lcrg(47)."""
import runpy, struct, sys, json
from collections import Counter

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


def rows_lcrg(raw):
    pos, rows = 14, []
    for j in range(2488):
        for k in range(200):
            ln = 41 + 5 * k
            end = pos + ln
            o, a, b = struct.unpack_from('<III', raw, end - 13)
            if o == j and a == b != 0 and raw[end - 1] == 0:
                rows.append(dict(row=j, ln=ln, k=k, biz=raw[pos:end - 13]))
                pos = end
                break
    return rows


print('#' * 30, 'WEATHER block structure')
raw = load('client', 27)
W = rows_weather(raw)
M = [r['mid'] for r in W]
n = len(M)
print('prefix b0..b2 all zero:', all(m[0:3] == b'\0\0\0' for m in M))
for b in range(4):
    d = 3 + 23 * b
    v = [m[d] for m in M]
    print(f'block{b} day@+0 (abs {d}): min={min(v)} max={max(v)} distinct={len(set(v))} '
          f'monotonic_ok={all(v[i] <= v[i+1] for i in range(0,0))}')
# monotonic day check per row
for b in range(4):
    d = 3 + 23 * b
    mono = sum(1 for m in M if b == 0 or m[3 + 23 * b] >= m[3 + 23 * (b - 1)])
    print(f'  day{b} >= day{b-1}: {mono}/{n}')
print('\nblock-internal: sum==100 windows (u8)')
for b in range(4):
    base = 3 + 23 * b
    for L in (5, 9, 10):
        for a in range(base, base + 23 - L + 1):
            c = sum(1 for m in M if sum(m[a:a + L]) == 100)
            if c >= 0.93 * n:
                print(f'  block{b} L={L} abs={a} rel={a-base} rate={c/n:.3f}')
print('\nblock0 byte profile (abs offset, rel, min,max,distinct,top3)')
for a in range(3, 26):
    v = [m[a] for m in M]
    print(f'  abs{a:2} rel{a-3:2} min={min(v):3} max={max(v):3} d={len(set(v)):3} '
          f'top={Counter(v).most_common(3)}')

print()
print('#' * 30, 'LCRG prefix structure')
raw = load('client', 47)
L = rows_lcrg(raw)
B = [r['biz'] for r in L]
print('rows', len(B))
print('b23 all zero:', all(b[23] == 0 for b in B))
print('b20 all zero:', all(b[20] == 0 for b in B))
print('b1..b3 all zero:', all(b[1:4] == b'\0\0\0' for b in B))
print('b22 == k all:', all(b[22] == r['k'] for b, r in zip(B, L)))
print('\n12 percentage bytes b8..b19 — group sums')
for g in range(3):
    a = 8 + 4 * g
    s = [sum(b[a:a + 4]) for b in B]
    print(f'  b{a}..b{a+3}: ==100 {sum(1 for x in s if x == 100)}/{len(B)} '
          f'<=100 {sum(1 for x in s if x <= 100)}/{len(B)} max={max(s)}')
print('\nsum of all 12 b8..b19:')
s = [sum(b[8:20]) for b in B]
print('  ==100:', sum(1 for x in s if x == 100), '<=100:', sum(1 for x in s if x <= 100),
      'max', max(s), 'distinct', len(set(s)))
print('\nb21 flag rows:', Counter(b[21] for b in B))
print('rows with b21==1: k values', Counter(r['k'] for b, r in zip(B, L) if b[21] == 1))
print('\nb0 (nation ordinal?) distinct', len({b[0] for b in B}), 'max', max(b[0] for b in B))
print('u32@4 (population?) zeros', sum(1 for b in B if int.from_bytes(b[4:8], 'little') == 0),
      'max', max(int.from_bytes(b[4:8], 'little') for b in B))
