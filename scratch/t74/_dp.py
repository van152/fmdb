"""Vectorized identity-triple DP (t57-style) with parent pointer reconstruction."""
import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct, collections

def scan_cands(raw, lo, hi, W=13, marker=True, align=None, pair=True):
    """dict ordinal -> sorted list of (id_start, uid)."""
    out = collections.defaultdict(list)
    for p in range(lo, hi - W + 1):
        if align is not None and (p % 4) != align:
            continue
        o, u1, u2 = struct.unpack_from('<III', raw, p)
        if pair and (u1 != u2 or u1 == 0):
            continue
        if marker and raw[p + W - 1] != 0:
            continue
        out[o].append((p, u1))
    for k in out:
        out[k].sort()
    return out

CACHE = {}
def _cand(raw, tag, lo, hi, W, marker, align, pair):
    key = (tag, lo, hi, W, marker, align, pair)
    if key not in CACHE:
        CACHE[key] = scan_cands(raw, lo, hi, W, marker, align, pair)
    return CACHE[key]

def dp_count(raw, tag, lo, hi, n, W=13, marker=True, align=None, pair=True, strict_uid=True):
    """reach[i] : row-start pos -> {uid_of_row_{i-1}: count}; reach[0][lo]={0:1}."""
    layers = _cand(raw, tag, lo, hi, W, marker, align, pair)
    reach = [dict() for _ in range(n + 1)]
    parent = [dict() for _ in range(n + 1)]   # (layer, endpos) -> (startpos, uid, prev_uid)
    reach[0][lo] = {0: 1}
    for i in range(n):
        nxt = {}
        lay = layers.get(i, [])
        for pos, uids in reach[i].items():
            for p0, uid in lay:
                if p0 < pos:
                    continue
                e = p0 + W
                if e > hi:
                    break
                for u, c in uids.items():
                    if strict_uid and uid <= u:
                        continue
                    d = nxt.setdefault(e, {})
                    d[uid] = d.get(uid, 0) + c
                    parent[i+1].setdefault((e, uid), (pos, uid, u))
        reach[i + 1] = nxt
        if not nxt:
            return 0, layers, reach, parent, i
    return sum(reach[n].get(hi, {}).values()), layers, reach, parent, n

def dp_walk(raw, tag, lo, hi, n, W=13, marker=True, align=None, pair=True, strict_uid=True):
    paths, layers, reach, parent, broke = dp_count(raw, tag, lo, hi, n, W, marker, align, pair, strict_uid)
    if not paths:
        return paths, None, layers, reach
    e = hi
    # choose any reaching uid at final
    uid = next(iter(reach[n][hi]))
    bounds = [None] * n
    for i in range(n, 0, -1):
        key = (e, uid)
        if key not in parent[i]:
            return paths, None, layers, reach
        pos, u_self, u_prev = parent[i][key]
        # identity starts at e - W
        bounds[i-1] = (pos, e, uid)
        e = pos
        uid = u_prev
    if e != lo:
        return paths, None, layers, reach
    return paths, bounds, layers, reach

if __name__ == '__main__':
    for arch, tid, n in [('client',8,126),('client',27,334),('client',18,1567),('client',7,208),
                         ('server',8,126),('server',27,334),('server',18,1567),('server',7,208)]:
        raw = load(arch, tid)
        p, b, lay, reach = dp_walk(raw, f'{arch}{tid}', 14, len(raw)-8, n)
        print(arch, tid, 'paths', p, 'walk', 'OK' if b else 'FAIL',
              'rowlens', [e-s for s,e,u in b[:4]] if b else None)
