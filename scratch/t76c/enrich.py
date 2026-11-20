"""t76c scratch: proper null model — hit rate vs uniform-draw chance over observed range."""
import runpy, struct, json, random
from pathlib import Path

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']
D = json.loads(Path('scratch/t76c/domains_client.json').read_text())
SETS = {k: set(v['uid_set']) for k, v in D.items()}


def chance(vals, S, trials=200):
    """Null: draw |vals| uniform integers from [min(vals), max(vals)]; hit rate."""
    lo, hi = min(vals), max(vals)
    if hi <= lo:
        return 0.0, 0.0
    rng = random.Random(20261120)
    out = []
    for _ in range(trials):
        d = [rng.randint(lo, hi) for _ in vals]
        out.append(sum(1 for x in d if x in S) / len(d))
    return sum(out) / len(out), max(out)


def test(label, vals, sets, nulls=('city', 'stadium', 'language', 'weather',
                                   'local_region', 'region', 'agreement')):
    vals = [x for x in vals if x != 0xFFFFFFFF]
    if len(vals) < 5:
        print(f'  {label}: too few ({len(vals)})')
        return {}
    res = {}
    for nm in nulls:
        S = sets[nm]
        obs = sum(1 for x in vals if x in S) / len(vals)
        c, cmax = chance(vals, S)
        res[nm] = (obs, c, cmax, obs - c)
    best = max(res.items(), key=lambda kv: kv[1][3])
    line = ' '.join(f'{nm}={res[nm][0]:.3f}(ch{res[nm][1]:.3f})' for nm in nulls)
    print(f'  {label}: n={len(vals)} range=[{min(vals)},{max(vals)}]\n     {line}')
    print(f'     BEST enrichment: {best[0]} obs={best[1][0]:.3f} chance={best[1][1]:.3f} '
          f'delta={best[1][3]:+.3f}')
    return res


# ---------- derby ----------
def derby_rows(arch):
    num = 36 if arch == 'client' else 42
    raw = load(arch, 18)
    pos, out = 14, []
    for j in range(1567):
        p, nb, names = pos, 0, []
        for _ in range(4):
            ln = struct.unpack_from('<I', raw, p)[0]
            names.append(raw[p + 4:p + 4 + ln].decode('utf-8'))
            nb += ln
            p += 4 + ln
        end = pos + 16 + nb + num + 13
        out.append(dict(row=j, names=names, num=raw[pos + 16 + nb:end - 13]))
        pos = end
    return out


DC = derby_rows('client')
print('=' * 25, 'DERBY client — 4CC FK candidates')
for off in (4, 8, 12, 16, 20):
    v = [int.from_bytes(r['num'][off:off + 4], 'little') for r in DC]
    test(f'u32@{off}', v, SETS)

# ---------- lcrg ----------
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
print('\n' + '=' * 25, 'LCRG client — prefix + item uids')
for off, w in ((0, 4), (4, 4)):
    v = [int.from_bytes(r['biz'][off:off + w], 'little') for r in R]
    test(f'u32@{off}', v, SETS)
v24 = [int.from_bytes(r['biz'][24:28], 'little') for r in R]
test('u32@24 (item0 uid)', v24, SETS)
items = []
for r in R:
    for i in range(r['k']):
        o = 28 + 5 * i
        items.append((r['biz'][o], int.from_bytes(r['biz'][o + 1:o + 5], 'little')))
test('item uid @28+5i', [x[1] for x in items], SETS)
