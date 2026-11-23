"""Sensitivity grid: identity width x alignment x footer, counting non-overlapping tilings."""
import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct, collections

def scan(raw, lo, hi, W, marker, align, pair):
    out = collections.defaultdict(list)
    for p in range(lo, hi - W + 1):
        if align is not None and (p - lo) % 4 != align:
            continue
        o, u1, u2 = struct.unpack_from('<III', raw, p)
        if pair and (u1 != u2 or u1 == 0):
            continue
        if marker and raw[p + W - 1] != 0:
            continue
        out[o].append((p, u1))
    for k in out: out[k].sort()
    return out

def tilings(raw, n, header, footer, W, marker, align, pair=True, strict_uid=True, cap=10**9):
    hi = len(raw) - footer
    layers = scan(raw, header, hi, W, marker, align, pair)
    if any(not layers.get(i) for i in range(n)):
        return 0, 'missing_layer'
    reach = [dict() for _ in range(n+1)]
    reach[0][header] = {0: 1}
    for i in range(n):
        nxt = {}
        for pos, uids in reach[i].items():
            for p0, uid in layers[i]:
                if p0 < pos: continue
                e = p0 + W
                if e > hi: break
                for u, c in uids.items():
                    if strict_uid and uid <= u: continue
                    d = nxt.setdefault(e, {})
                    d[uid] = min(cap, d.get(uid, 0) + c)
        reach[i+1] = nxt
        if not nxt: return 0, f'break@{i}'
    return sum(reach[n].get(hi, {}).values()), 'ok'

TABLES = [('client',0,3545),('client',56,6),('client',8,126),('server',8,126),
          ('client',7,208),('server',7,208),('client',18,1567),('server',18,1567),
          ('client',27,334),('server',27,334),('client',47,2488),('server',47,2488)]

if __name__ == '__main__':
    for arch, tid, n in TABLES:
        raw = load(arch, tid)
        print(f'=== {arch} t{tid} n={n} len={len(raw)}')
        for foot in (7,8,9,10,12):
            line = []
            for W, mk in ((12,False),(13,True)):
                cnts = []
                for align in (0,1,2,3,None):
                    v, st = tilings(raw, n, 14, foot, W, mk, align)
                    cnts.append(v)
                line.append(f'W{W}{"m" if mk else " "}={cnts}')
            print(f'  foot={foot:2d}  ' + '  '.join(line))
