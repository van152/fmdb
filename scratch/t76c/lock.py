"""t76c scratch: final number lock — calibration cross-checks + lcrg/weather slot table."""
import runpy, struct
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']

N = {'club': 84259, 'team': 84507, 'comp': 7047, 'stadium': 48413, 'city': 56293,
     'nation': 251, 'region': 28, 'continent': 7, 'language': 126, 'weather': 334,
     'local_region': 2488, 'agreement': 6}


def colf(raw, H, S, n, off, w=4):
    return [int.from_bytes(raw[H + j * S + off:H + j * S + off + w], 'little')
            for j in range(n)]


print('=== CALIBRATION cross-check on more frozen anchors')
raw2 = load('client', 2)
for name, off, w in (('Clri@25', 25, 2), ('Clgi@21', 21, 2), ('Cwea@14', 14, 2),
                     ('Catt@9', 9, 1), ('Cnti@10', 10, 2)):
    v = colf(raw2, 14, 43, 56293, off, w)
    mx = max(x for x in v if x != (1 << (8 * w)) - 1) if any(
        x != (1 << (8 * w)) - 1 for x in v) else 0
    print(f'  {name}: w={w} distinct={len(set(v))} min={min(v)} max={max(v)} '
          f'max_nonnull={mx}')
    for nm in ('city', 'nation', 'weather', 'local_region', 'region', 'stadium'):
        lim = N[nm]
        if mx < lim:
            print(f'      fits {nm}(N={lim}) max/N={mx/lim:.3f}')

print('\n=== LCRG prefix full table (client)')
def rows_lcrg(raw):
    pos, out = 14, []
    for j in range(2488):
        for k in range(200):
            ln = 41 + 5 * k
            end = pos + ln
            o, a, b = struct.unpack_from('<III', raw, end - 13)
            if o == j and a == b != 0 and raw[end - 1] == 0:
                out.append(dict(row=j, ln=ln, k=k, biz=raw[pos:end - 13]))
                pos = end
                break
    return out


R = rows_lcrg(load('client', 47))
print('  biz_len == 28 + 5k:', all(len(r['biz']) == 28 + 5 * r['k'] for r in R))
print('  b22 == k:', all(r['biz'][22] == r['k'] for r in R))
print('  b23 == 0:', all(r['biz'][23] == 0 for r in R))
print('  b20 == 0:', all(r['biz'][20] == 0 for r in R))
for off, w in ((0, 4), (4, 4)):
    v = [int.from_bytes(r['biz'][off:off + w], 'little') for r in R]
    print(f'  u32@{off}: distinct={len(set(v))} min={min(v)} max={max(v)} '
          f'zero={v.count(0)} ff={v.count(0xFFFFFFFF)}')
for nm in ('nation', 'local_region', 'weather', 'club', 'city'):
    lim = N[nm]
    v0 = [int.from_bytes(r['biz'][0:4], 'little') for r in R]
    print(f'    u32@0 fits {nm}(N={lim}): {sum(1 for x in v0 if x < lim)}/{len(v0)}')
v4 = [int.from_bytes(r['biz'][4:8], 'little') for r in R]
print(f'  u32@4 (Lpop): max={max(v4)} zeros={v4.count(0)} '
      f'<=1e9={sum(1 for x in v4 if x <= 10**9)}/{len(v4)}')
print('  items: k × 5B at offset 28')
it = []
for r in R:
    for i in range(r['k']):
        o = 28 + 5 * i
        it.append((r['biz'][o], int.from_bytes(r['biz'][o + 1:o + 5], 'little')))
print(f'    n={len(it)} pct 0..100: {sum(1 for p,_ in it if p<=100)}/{len(it)} '
      f'pct distinct={len({p for p,_ in it})}')
u = [x for _, x in it if x != 0xFFFFFFFF]
print(f'    uid null={sum(1 for _,x in it if x==0xFFFFFFFF)} nonnull={len(u)} '
      f'distinct={len(set(u))} min={min(u)} max={max(u)}')
for nm in ('language', 'nation', 'weather', 'city', 'region'):
    lim = N[nm]
    print(f'      uid < {nm}(N={lim}): {sum(1 for x in u if x < lim)}/{len(u)}')

print('\n=== WEATHER: exact block arithmetic + block0 field table')
raw = load('client', 27)
M, pos, NL = [], 14, []
for j in range(334):
    ln = struct.unpack_from('<I', raw, pos)[0]
    end = pos + 4 + ln + 95 + 13
    M.append(raw[pos + 4 + ln:end - 13])
    NL.append(ln)
    pos = end
print('  95 == 3 + 4*23 ?', 95 == 3 + 4 * 23)
print('  namelen range', min(NL), max(NL), 'distinct', len(set(NL)))
print('  prefix 3B zero for all rows:', all(m[0:3] == b'\0\0\0' for m in M))
for b in range(4):
    base = 3 + 23 * b
    p = [sum(1 for m in M if sum(m[base + 2:base + 7]) == 100)]
    w = [sum(1 for m in M if sum(m[base + 7:base + 12]) == 100)]
    t = [sum(1 for m in M if sum(m[base + 12:base + 22]) == 100)]
    print(f'  block{b}: precip sum100={p[0]}/334 wind sum100={w[0]}/334 '
          f'temp10 sum100={t[0]}/334')
print('\n  block0 rel map:')
for rel in range(23):
    v = [m[3 + rel] for m in M]
    print(f'    rel{rel:2} d={len(set(v)):3} min={min(v):3} max={max(v):3} '
          f'zero={v.count(0):3} top={Counter(v).most_common(2)}')
