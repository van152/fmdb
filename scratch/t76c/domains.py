"""t76c scratch: build live reference domains (ordinal range + UID set where walkable)."""
import runpy, struct, sys, json
from pathlib import Path

core = runpy.run_path('scripts/t73_mapper_core.py', run_name='probe')
load = core['load_payload']


def u32(raw, off):
    return struct.unpack_from('<I', raw, off)[0]


def fixed_rows(raw, H, S, n, p):
    """Yield (row_index, duni) for a fixed-stride table whose identity holds."""
    ok = True
    out = []
    for j in range(n):
        b = H + j * S + p
        o, a, bb = u32(raw, b), u32(raw, b + 4), u32(raw, b + 8)
        if not (o == j and a == bb != 0):
            ok = False
        out.append((j, a))
    return out, ok


def ident_var(raw, pos, ln, j):
    t = pos + ln - 13
    o, a, b = struct.unpack_from('<III', raw, t)
    return (o == j and a == b != 0 and raw[t + 12] == 0), a


def build(arch='client'):
    doms = {}
    # city 2: 43 fixed, identity @30
    raw = load(arch, 2)
    rows, ok = fixed_rows(raw, 14, 43, 56293, 30)
    doms['city'] = {'n': 56293, 'uids': [r[1] for r in rows], 'ok': ok, 'tid': 2}
    # stadium 21 client: 38 fixed identity @25; server 181 @169
    if arch == 'client':
        raw = load(arch, 21)
        rows, ok = fixed_rows(raw, 14, 38, 48413, 25)
    else:
        raw = load(arch, 21)
        rows, ok = fixed_rows(raw, 14, 181, 48413, 169)
    doms['stadium'] = {'n': 48413, 'uids': [r[1] for r in rows], 'ok': ok, 'tid': 21}
    # region 19 client: 45 fixed identity @32; server 46 @33
    raw = load(arch, 19)
    if arch == 'client':
        rows, ok = fixed_rows(raw, 14, 45, 28, 32)
    else:
        rows, ok = fixed_rows(raw, 14, 46, 28, 33)
    doms['region'] = {'n': 28, 'uids': [r[1] for r in rows], 'ok': ok, 'tid': 19}
    # continent 5
    raw = load(arch, 5)
    rows, ok = fixed_rows(raw, 14, 34 if arch == 'client' else 48, 7,
                          21 if arch == 'client' else 35)
    doms['continent'] = {'n': 7, 'uids': [r[1] for r in rows], 'ok': ok, 'tid': 5}
    # language 8: variable u32 len + name + 17B + 13B identity
    raw = load(arch, 8)
    pos, uids, ok = 14, [], True
    for j in range(126):
        ln = u32(raw, pos)
        end = pos + 4 + ln + 17 + 13
        good, uid = ident_var(raw, end - 13, 13, j)
        ok = ok and good
        uids.append(uid)
        pos = end
    doms['language'] = {'n': 126, 'uids': uids, 'ok': ok and pos + 8 == len(raw), 'tid': 8}
    # weather 27: u32 len + name + 95 + 13
    raw = load(arch, 27)
    pos, uids, ok = 14, [], True
    for j in range(334):
        ln = u32(raw, pos)
        end = pos + 4 + ln + 95 + 13
        good, uid = ident_var(raw, end - 13, 13, j)
        ok = ok and good
        uids.append(uid)
        pos = end
    doms['weather'] = {'n': 334, 'uids': uids, 'ok': ok and pos + 8 == len(raw), 'tid': 27}
    # local_region 47: lcrg tail
    raw = load(arch, 47)
    pos, uids, ok = 14, [], True
    for j in range(2488):
        hit = None
        for k in range(200):
            ln = 41 + 5 * k
            good, uid = ident_var(raw, pos, ln, j)
            if good:
                hit = (ln, uid)
                break
        if hit is None:
            ok = False
            break
        uids.append(hit[1])
        pos += hit[0]
    doms['local_region'] = {'n': 2488, 'uids': uids, 'ok': ok and pos + 8 == len(raw),
                            'tid': 47}
    # agreement 56: 13 fixed
    raw = load(arch, 56)
    rows, ok = fixed_rows(raw, 14, 13, 6, 0)
    doms['agreement'] = {'n': 6, 'uids': [r[1] for r in rows], 'ok': ok, 'tid': 56}
    # comp 25: try fixed 127 client identity @114 / server stride?
    out = {}
    for nm, d in doms.items():
        u = d.pop('uids')
        out[nm] = d | {'uid_set': set(u), 'uid_sample': u[:5], 'distinct_uids': len(set(u))}
    return out


if __name__ == '__main__':
    for arch in ('client', 'server'):
        d = build(arch)
        print('=' * 20, arch)
        for nm, v in d.items():
            print(f'  {nm:14} tid={v["tid"]:<3} n={v["n"]:<7} identity_ok={v["ok"]} '
                  f'distinct_uids={v["distinct_uids"]}')
        Path(f'scratch/t76c/domains_{arch}.json').write_text(
            json.dumps({k: {kk: (sorted(vv) if kk == 'uid_set' else vv)
                            for kk, vv in v.items()} for k, v in d.items()}),
            encoding='utf-8')
