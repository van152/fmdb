"""t76c scratch: FK test with REAL uid sets (not just dense ordinal ranges)."""
import runpy, struct, json, sys
from pathlib import Path

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']
D = json.loads(Path('scratch/t76c/domains_client.json').read_text())
CITY = set(D['city']['uid_set'])
STAD = set(D['stadium']['uid_set'])
LANG = set(D['language']['uid_set'])
WEAT = set(D['weather']['uid_set'])
LCRG = set(D['local_region']['uid_set'])
REGN = set(D['region']['uid_set'])


def rows_lcrg(raw):
    pos, rows = 14, []
    for j in range(2488):
        for k in range(200):
            ln = 41 + 5 * k
            end = pos + ln
            o, a, b = struct.unpack_from('<III', raw, end - 13)
            if o == j and a == b != 0 and raw[end - 1] == 0:
                rows.append(dict(row=j, ln=ln, k=k, biz=raw[pos:end - 13],
                                 uid=a))
                pos = end
                break
    return rows


raw = load('client', 47)
R = rows_lcrg(raw)
print('=== lcrg: biz_len == 23 + 5*(k+1)?',
      all(len(r['biz']) == 23 + 5 * (r['k'] + 1) for r in R))

# items from offset 23
items = []
for r in R:
    b = r['biz']
    for i in range(r['k'] + 1):
        o = 23 + 5 * i
        items.append((r['row'], i, b[o], int.from_bytes(b[o + 1:o + 5], 'little'), r['k']))
print('total items', len(items))
for slot in (0, 1, 2):
    sel = [it for it in items if it[1] == slot]
    if not sel:
        continue
    u = [it[3] for it in sel]
    p = [it[2] for it in sel]
    nn = [x for x in u if x != 0xFFFFFFFF]
    print(f' item{slot}: n={len(sel)} pct_set={sorted(set(p))[:8]} '
          f'uid_null={u.count(0xFFFFFFFF)} distinct_uid={len(set(nn))}')
    for nm, S in (('city', CITY), ('stadium', STAD), ('language', LANG),
                  ('weather', WEAT), ('region', REGN), ('local_region', LCRG)):
        print(f'    in {nm} set: {sum(1 for x in nn if x in S)}/{len(nn)}')

# all items except slot0 (i.e. the Lrll list body)
body = [it for it in items if it[1] >= 1]
u = [it[3] for it in body]
nn = [x for x in u if x != 0xFFFFFFFF]
print(f'\nbody items: n={len(body)} null={u.count(0xFFFFFFFF)} nonnull={len(nn)} '
      f'distinct={len(set(nn))}')
for nm, S in (('language', LANG), ('city', CITY), ('nation251-range', None)):
    if S is not None:
        print(f'  in {nm} set: {sum(1 for x in nn if x in S)}/{len(nn)}')

# prefix downward: @24 u32 (slot0 uid) vs sets
u24 = [int.from_bytes(r['biz'][24:28], 'little') for r in R]
nn24 = [x for x in u24 if x != 0xFFFFFFFF]
print(f'\n@24 u32: null={u24.count(0xFFFFFFFF)} nonnull={len(nn24)} distinct={len(set(nn24))} '
      f'min={min(nn24)} max={max(nn24)}')
for nm, S in (('city', CITY), ('weather', WEAT), ('region', REGN),
              ('stadium', STAD), ('language', LANG)):
    print(f'  in {nm} set: {sum(1 for x in nn24 if x in S)}/{len(nn24)}')

print('\n=== lcrg prefix byte columns b0..b22')
for off in range(23):
    v = [r['biz'][off] for r in R]
    print(f'  b{off:2}: d={len(set(v)):4} min={min(v):3} max={max(v):3} '
          f'zero={v.count(0):5} ff={v.count(255):4}')
print('\n  u32@0 (b0..b3) values distinct', len({int.from_bytes(r['biz'][0:4], "little") for r in R}),
      'max', max(int.from_bytes(r['biz'][0:4], 'little') for r in R))
print('  u32@4 max', max(int.from_bytes(r['biz'][4:8], 'little') for r in R),
      'zeros', sum(1 for r in R if int.from_bytes(r['biz'][4:8], 'little') == 0))
for off in (8, 12, 16, 20):
    v = [int.from_bytes(r['biz'][off:off + 4], 'little') for r in R]
    print(f'  u32@{off}: distinct={len(set(v))} max={max(v)} zero={v.count(0)} ff={v.count(0xFFFFFFFF)}')

print('\n=== derby: Dfms (u32@16) vs real stadium set; Dfmc vs range')
NUM = {'client': 36, 'server': 42}
raw = load('client', 18)
pos, DD = 14, []
for j in range(1567):
    p, nb = pos, 0
    for _ in range(4):
        ln = struct.unpack_from('<I', raw, p)[0]
        nb += ln
        p += 4 + ln
    end = pos + 16 + nb + 36 + 13
    DD.append(raw[pos + 16 + nb:end - 13])
    pos = end
v16 = [int.from_bytes(d[16:20], 'little') for d in DD]
v16nn = [x for x in v16 if x != 0xFFFFFFFF]
print(f'  @16: null={v16.count(0xFFFFFFFF)} nonnull={len(v16nn)} distinct={len(set(v16nn))} '
      f'max={max(v16nn)}')
print(f'    in stadium set: {sum(1 for x in v16nn if x in STAD)}/{len(v16nn)}')
print(f'    in city set:    {sum(1 for x in v16nn if x in CITY)}/{len(v16nn)}')
print(f'    in language set:{sum(1 for x in v16nn if x in LANG)}/{len(v16nn)}')
v12 = [int.from_bytes(d[12:16], 'little') for d in DD]
v12nn = [x for x in v12 if x != 0xFFFFFFFF]
print(f'  @12: null={v12.count(0xFFFFFFFF)} nonnull={len(v12nn)} distinct={len(set(v12nn))} '
      f'max={max(v12nn)}')
for nm, S in (('stadium', STAD), ('city', CITY), ('language', LANG), ('weather', WEAT)):
    print(f'    in {nm} set: {sum(1 for x in v12nn if x in S)}/{len(v12nn)}')
