"""t76c scratch: decide the 95B weather middle layout — 4x23 vs 3+4x22+4."""
import runpy, struct
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
raw = core['load_payload']('client', 27)
M, pos = [], 14
for j in range(334):
    ln = struct.unpack_from('<I', raw, pos)[0]
    end = pos + 4 + ln + 95 + 13
    M.append(raw[pos + 4 + ln:end - 13])
    pos = end
n = len(M)


def score(prefix, blk, k=4, tail=0):
    """How cleanly does the hypothesis reproduce sum==100 for the 3 groups?"""
    tot = 0
    detail = []
    for b in range(k):
        base = prefix + blk * b
        p = [sum(m[base + 1:base + 6]) for m in M]
        w = [sum(m[base + 6:base + 11]) for m in M]
        t = [sum(m[base + 11:base + 21]) for m in M]
        detail.append((p.count(100), w.count(100), t.count(100)))
        tot += p.count(100) + w.count(100) + t.count(100)
    return tot, detail


for prefix, blk, tail, name in ((3, 23, 0, '3 + 4x23'),
                                (3, 22, 4, '3 + 4x22 + 4'),
                                (0, 23, 3, '4x23 + 3')):
    if prefix + blk * 4 + tail != 95:
        continue
    tot, det = score(prefix, blk)
    print(f'{name:14} total_sum100={tot}/12*334={12*n} '
          f'per-block={det}')

print('\n--- hypothesis B: 3 + 4x22 + 4  (field map block0)')
for rel in range(22):
    v = [m[3 + rel] for m in M]
    print(f'  rel{rel:2} d={len(set(v)):3} min={min(v):3} max={max(v):3} z={v.count(0):3}')
print('  trailing 4 bytes @91..94, per byte:')
for i in range(4):
    v = [m[91 + i] for m in M]
    print(f'    b{91+i}: {Counter(v).most_common(3)}')
print('\n--- under A (3+4x23) the bytes at 3+23b+22 for b=0..3 were identical:')
print('   that is byte 25,48,71,94 -- under B those are 25,47,69,91 -> mixed meaning')
print('   decisive test: is byte 94 (last of mid) == byte 25/48/71?')
print('   ', all(M[j][25] == M[j][48] == M[j][71] == M[j][94] for j in range(n)))
print('   byte 91..94 equal?', all(M[j][91] == M[j][92] == M[j][93] == M[j][94] for j in range(n)))
print('   which bytes are constant across all 334 rows?',
      [o for o in range(95) if len({m[o] for m in M}) == 1])
print('   which bytes take only {0,100}?',
      [o for o in range(95) if {m[o] for m in M} <= {0, 100} and len({m[o] for m in M}) == 2])
