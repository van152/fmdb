"""t76c scratch: weather 23B block field mapping test."""
import runpy, struct
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']

raw = load('client', 27)
M, pos = [], 14
for j in range(334):
    ln = struct.unpack_from('<I', raw, pos)[0]
    end = pos + 4 + ln + 95 + 13
    M.append(raw[pos + 4 + ln:end - 13])
    pos = end
n = len(M)
print('rows', n, 'mid', len(M[0]))
print('prefix [0,3) all zero:', all(m[0:3] == b'\0\0\0' for m in M))
print('3 + 4*23 =', 3 + 4 * 23)

for b in range(4):
    base = 3 + 23 * b
    blk = [m[base:base + 23] for m in M]
    print(f'\n--- block{b} base={base}')
    for rel in range(23):
        v = [x[rel] for x in blk]
        print(f'  rel{rel:2} d={len(set(v)):3} min={min(v):3} max={max(v):3} '
              f'z={v.count(0):4} top={Counter(v).most_common(2)}')
    # structured tests
    s5 = [sum(x[2:7]) for x in blk]
    s5b = [sum(x[7:12]) for x in blk]
    s10 = [sum(x[12:22]) for x in blk]
    print(f'  sum rel2..6  ==100: {sum(1 for s in s5 if s == 100)}/{n} min={min(s5)} max={max(s5)}')
    print(f'  sum rel7..11 ==100: {sum(1 for s in s5b if s == 100)}/{n} min={min(s5b)} max={max(s5b)}')
    print(f'  sum rel12..21==100: {sum(1 for s in s10 if s == 100)}/{n} min={min(s10)} max={max(s10)}')
    print(f'  rel22 values {Counter(x[22] for x in blk).most_common(4)}')
    print(f'  rel1  values {Counter(x[1] for x in blk).most_common(4)}')
