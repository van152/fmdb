"""t76c scratch: last decisive batch — derby tail fields, weather block map, lcrg @24."""
import runpy, struct
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']


def derby_num(arch):
    num = 36 if arch == 'client' else 42
    raw = load(arch, 18)
    pos, out = 14, []
    for j in range(1567):
        p, nb = pos, 0
        for _ in range(4):
            ln = struct.unpack_from('<I', raw, p)[0]
            nb += ln
            p += 4 + ln
        end = pos + 16 + nb + num + 13
        out.append(raw[pos + 16 + nb:end - 13])
        pos = end
    return out


DC = derby_num('client')
print('=== DERBY client tail: b28/b29 non-null ranges (D1tw/D1td/D1tl candidates)')
for off in (28, 29):
    v = [d[off] for d in DC]
    nn = [x for x in v if x != 255]
    print(f'  b{off}: null(255)={v.count(255)} nonnull={len(nn)} min={min(nn)} '
          f'max={max(nn)} distinct={len(set(nn))} values={sorted(set(nn))[:16]}')
print('  u16@28 non-null max:', max(int.from_bytes(d[28:30], 'little') for d in DC
                                  if d[28:30] != b'\xff\xff'))
print('\n=== DERBY b34/b35 (schema Dwdr/Dntr: min 0 max 200)')
for off in (34, 35):
    v = [d[off] for d in DC]
    print(f'  b{off}: min={min(v)} max={max(v)} distinct={len(set(v))} zero={v.count(0)} '
          f'<=200:{sum(1 for x in v if x<=200)}/{len(v)}')
print('  both-zero rows:', sum(1 for d in DC if d[34] == 0 and d[35] == 0))
print('  b34 != b35 rows:', sum(1 for d in DC if d[34] != d[35]))

print('\n=== DERBY: which slots are non-null (not 0xffffffff)')
for off in (12, 16, 20):
    v = [int.from_bytes(d[off:off + 4], 'little') for d in DC]
    print(f'  u32@{off}: nonnull={sum(1 for x in v if x != 0xFFFFFFFF)}')
# co-occurrence of @12,@16,@20 non-null
pat = Counter(tuple(int.from_bytes(d[o:o + 4], 'little') != 0xFFFFFFFF for o in (12, 16, 20))
              for d in DC)
print('  nonnull pattern (@12,@16,@20):', pat.most_common())

print('\n=== WEATHER block0 deep map: are rel2..6 and rel7..11 disjoint 5-sets?')
raw = load('client', 27)
M, pos = [], 14
for j in range(334):
    ln = struct.unpack_from('<I', raw, pos)[0]
    end = pos + 4 + ln + 95 + 13
    M.append(raw[pos + 4 + ln:end - 13])
    pos = end
for b in range(4):
    base = 3 + 23 * b
    print(f'  block{b}: rel0={base}')
    for rel in range(23):
        v = [m[base + rel] for m in M]
        print(f'    rel{rel:2} d={len(set(v)):3} min={min(v):3} max={max(v):3} '
              f'z={v.count(0):3}')

print('\n=== LCRG: is u32@24 == u32@0?')
def rows_lcrg(raw):
    pos, out = 14, []
    for j in range(2488):
        for k in range(200):
            ln = 41 + 5 * k
            end = pos + ln
            o, a, b = struct.unpack_from('<III', raw, end - 13)
            if o == j and a == b != 0 and raw[end - 1] == 0:
                out.append(raw[pos:end - 13])
                pos = end
                break
    return out


R = rows_lcrg(load('client', 47))
v0 = [int.from_bytes(r[0:4], 'little') for r in R]
v24 = [int.from_bytes(r[24:28], 'little') for r in R]
print('  equal:', sum(1 for a, b in zip(v0, v24) if a == b), '/', len(R))
print('  both null:', sum(1 for a, b in zip(v0, v24) if a == 0xFFFFFFFF and b == 0xFFFFFFFF))
print('  u32@24 null count', v24.count(0xFFFFFFFF), 'u32@0 null', v0.count(0xFFFFFFFF))
print('  u32@24 nonnull max', max(x for x in v24 if x != 0xFFFFFFFF))
print('  rows with k==0: b24..b27 =', Counter(R[i][24:28].hex() for i in range(len(R))
                                             if R[i][22] == 0).most_common(3))
