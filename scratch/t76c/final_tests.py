"""t76c scratch: decisive lcrg reference tests + weather temperature window."""
import runpy, struct, json, random
from collections import Counter
from pathlib import Path

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']
D = json.loads(Path('scratch/t76c/domains_client.json').read_text())
LANG = set(D['language']['uid_set'])
CITY = set(D['city']['uid_set'])
WEAT = set(D['weather']['uid_set'])


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


def ctrl(vals, S, trials=60):
    rng = random.Random(76)
    v = list(vals)
    obs = sum(1 for x in v if x in S) / max(1, len(v))
    sh = []
    for _ in range(trials):
        rng.shuffle(v)
        sh.append(sum(1 for x in v if x in S) / max(1, len(v)))
    return obs, sum(sh) / len(sh), max(sh)


print('=== lcrg items (u8 pct, u32 uid) at offset 28, k items')
items = []
for r in R:
    b = r['biz']
    for i in range(r['k']):
        o = 28 + 5 * i
        items.append((b[o], int.from_bytes(b[o + 1:o + 5], 'little')))
print(' items', len(items), '== sum k', sum(r['k'] for r in R))
u = [x[1] for x in items]
p = [x[0] for x in items]
nn = [x for x in u if x != 0xFFFFFFFF]
print(f' pct<=100: {sum(1 for x in p if x <= 100)}/{len(p)}  pct distinct {len(set(p))}')
print(f' uid: null={u.count(0xFFFFFFFF)} nonnull={len(nn)} distinct={len(set(nn))}')
for nm, S in (('language', LANG), ('city', CITY), ('weather', WEAT)):
    o, m, mx = ctrl(nn, S)
    print(f'  vs {nm:9}: hit={o:.4f} shuffle_mean={m:.4f} shuffle_max={mx:.4f} '
          f'-> {"SIGNAL" if o > mx + 0.05 else "no-signal"}')
print('  nonnull pct top', Counter(x[0] for x in items if x[1] != 0xFFFFFFFF).most_common(8))

print('\n=== lcrg u32@24 (scalar before items)')
v24 = [int.from_bytes(r['biz'][24:28], 'little') for r in R]
nn24 = [x for x in v24 if x != 0xFFFFFFFF]
print(f' null={v24.count(0xFFFFFFFF)} nonnull={len(nn24)} distinct={len(set(nn24))} '
      f'min={min(nn24)} max={max(nn24)}')
for nm, S in (('language', LANG), ('city', CITY), ('weather', WEAT)):
    o, m, mx = ctrl(nn24, S)
    print(f'  vs {nm:9}: hit={o:.4f} shuffle_max={mx:.4f}')

print('\n=== lcrg u32@0 (nation ordinal domain test, nation=251 rows)')
v0 = [int.from_bytes(r['biz'][0:4], 'little') for r in R]
print(f' distinct={len(set(v0))} min={min(v0)} max={max(v0)} <251={sum(1 for x in v0 if x<251)}/{len(v0)}')

print('\n=== lcrg b8..b19: 12 independent 0..100 bytes; joint sum stats')
for i in range(8, 20):
    v = [r['biz'][i] for r in R]
    print(f'  b{i}: d={len(set(v)):3} min={min(v):3} max={max(v):3} zero={v.count(0)}')
print('  b21 flag rows', Counter(r['biz'][21] for r in R))
print('  rows where b21==1: k', Counter(r['k'] for r in R if r['biz'][21] == 1))

print('\n' + '=' * 20, 'WEATHER temperature window search')
raw = load('client', 27)
M, pos = [], 14
for j in range(334):
    ln = struct.unpack_from('<I', raw, pos)[0]
    end = pos + 4 + ln + 95 + 13
    M.append(raw[pos + 4 + ln:end - 13])
    pos = end
for b in range(4):
    base = 3 + 23 * b
    for start in range(base + 1, base + 14):
        for L in (9, 10):
            if start + L > base + 23:
                continue
            c = sum(1 for m in M if sum(m[start:start + L]) == 100)
            if c >= 0.9 * 334:
                print(f'  block{b} base={base} start={start} rel={start-base} L={L} '
                      f'exact100={c}/334')
print('\n block0 rel12 constant?', Counter(m[15] for m in M).most_common(3))
print(' block0 rel22:', Counter(m[25] for m in M).most_common(3))
print(' rel22==100 count per block:',
      [sum(1 for m in M if m[3 + 23 * b + 22] == 100) for b in range(4)])
