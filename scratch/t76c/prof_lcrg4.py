"""t76c scratch: lcrg 5-byte item ordering — pct-first vs uid-first, with null sentinel."""
import runpy, struct, sys
from collections import Counter

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']

LANG_N = 126
CITY_N = 56293
NATION_N = 251


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
    return round(sum(1 for v in vals if v < n) / max(1, len(vals)), 4)


def report(name, groups):
    u = [g[1] for g in groups]
    p = [g[0] for g in groups]
    print(f'{name}: n={len(u)} pct<=100 {rate(p, 101)} pct255 {p.count(255)} '
          f'uid_null {u.count(0xFFFFFFFF)} uid<126 {rate(u, LANG_N)} '
          f'uid<251 {rate(u, NATION_N)} uid<56293 {rate(u, CITY_N)}')


# D: prefix 28, k items (u8 pct, u32 uid)
D = []
for r in rows:
    b = r['biz'][28:]
    D += [(b[i], int.from_bytes(b[i + 1:i + 5], 'little')) for i in range(0, len(b), 5)]
report('D prefix28 (pct,u32)', D)

# E: prefix 23, k+1 items (u8 pct, u32 uid) — item0 pct always 0?
E0, Erest = [], []
for r in rows:
    b = r['biz'][23:]
    g = [(b[i], int.from_bytes(b[i + 1:i + 5], 'little')) for i in range(0, len(b), 5)]
    E0.append(g[0]); Erest += g[1:]
report('E item0 (pct,u32)', E0)
report('E rest  (pct,u32)', Erest)
print('E item0 pct set', sorted({g[0] for g in E0}))
print('E item0 uid sample', sorted({g[1] for g in E0})[:12],
      'distinct', len({g[1] for g in E0}), 'null', sum(1 for g in E0 if g[1] == 0xFFFFFFFF))

# which uids repeat? language table uids
lang = core['reference_uids']('client', 8) if False else None
print()
print('=== E item0 uid vs city/nation/lang domain hit-rate')
for nm, n in (('lang126', LANG_N), ('nation251', NATION_N), ('city56293', CITY_N),
              ('weather334', 334), ('region28', 28), ('stadium48413', 48413)):
    print(f'  {nm}: {rate([g[1] for g in E0], n)}')
print()
print('=== E rest uid vs domains')
for nm, n in (('lang126', LANG_N), ('nation251', NATION_N), ('city56293', CITY_N),
              ('region28', 28)):
    print(f'  {nm}: {rate([g[1] for g in Erest], n)}')
print()
print('E rest pct distribution', Counter(g[0] for g in Erest).most_common(10))
print('E rest null uids', sum(1 for g in Erest if g[1] == 0xFFFFFFFF), '/', len(Erest))
