"""t76c scratch: unique-best window per group per block + dn search."""
import runpy, struct

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
raw = core['load_payload']('client', 27)
M, pos = [], 14
for j in range(334):
    ln = struct.unpack_from('<I', raw, pos)[0]
    end = pos + 4 + ln + 95 + 13
    M.append(raw[pos + 4 + ln:end - 13])
    pos = end
n = len(M)

for b in range(4):
    base = 3 + 23 * b
    print(f'=== block{b} (base={base})')
    for L, label in ((5, 'precip/wind'), (10, 'temp')):
        res = []
        for o in range(0, 24 - L):
            s = [sum(m[base + o:base + o + L]) for m in M]
            res.append((s.count(100), o))
        res.sort(reverse=True)
        print(f'  best {label} L={L}: ' +
              ', '.join(f'rel{o}({c})' for c, o in res[:4]))

# Does the 10-byte temp group have a per-block scale?
print('\n=== temp sum histogram (rel12..21) per block')
from collections import Counter
for b in range(4):
    base = 3 + 23 * b
    s = [sum(m[base + 12:base + 22]) for m in M]
    print(f'  block{b}:', Counter(s).most_common(8))

# Is block1 temp maybe 2-byte values summing differently? check parity structure
print('\n=== block1 rel12..21 detail')
for rel in range(12, 22):
    v = [m[26 + rel] for m in M]
    print(f'  rel{rel}: d={len(set(v))} [{min(v)},{max(v)}] z={v.count(0)}')
print('  block1 rows where temp sum==0:', sum(1 for m in M if sum(m[38:48]) == 0))
print('  block1 rows where temp sum in (95,105):',
      sum(1 for m in M if 95 <= sum(m[38:48]) <= 105))
print('  block1 rows where temp sum > 105:', sum(1 for m in M if sum(m[38:48]) > 105))
print('  block0 same:', sum(1 for m in M if sum(m[15:25]) > 105),
      '/ block2:', sum(1 for m in M if sum(m[61:71]) > 105),
      '/ block3:', sum(1 for m in M if sum(m[84:94]) > 105))
