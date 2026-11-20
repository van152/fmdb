"""t76c scratch: weather block - examine rows where sums != 100."""
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

print('=== precip rel2..6 failures (sum != 100)')
bad = [(i, M[i][3:26], sum(M[i][5:10])) for i in range(n) if sum(M[i][5:10]) != 100]
for i, blk, s in bad[:12]:
    print(f'  row{i} sum={s} block0={blk.hex(" ")}')
print('  total failures', len(bad), 'sum distribution', Counter(s for _, _, s in bad))

print('\n=== wind rel7..11 failures')
bad2 = [(i, sum(M[i][10:15])) for i in range(n) if sum(M[i][10:15]) != 100]
print('  total', len(bad2), 'sums', Counter(s for _, s in bad2).most_common(8))

print('\n=== temp rel12..21 sums distribution')
st = [sum(M[i][15:25]) for i in range(n)]
print('  ', Counter(st).most_common(10), 'exact100', st.count(100))

print('\n=== block0 rel12 =', Counter(M[i][15] for i in range(n)))

# Check whether failures are only in later blocks (b=0 base 3)
print('\n=== per-block precip sum==100 rate')
for b in range(4):
    base = 3 + 23 * b
    c = sum(1 for m in M if sum(m[base + 2:base + 7]) == 100)
    c2 = sum(1 for m in M if sum(m[base + 7:base + 12]) == 100)
    c3 = sum(1 for m in M if sum(m[base + 12:base + 22]) == 100)
    print(f'  block{b}: precip {c}/{n} wind {c2}/{n} temp {c3}/{n}')
