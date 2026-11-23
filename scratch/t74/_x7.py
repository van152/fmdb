"""Exploration: layered identity-triple DP tiling (corrected)."""
import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct, collections

def build_cands(raw, lo, hi, W, align=None, require_marker=False, require_uid_eq=True):
    """(p, ordinal, uid) where a W-byte identity trailer starts at p."""
    out = collections.defaultdict(list)
    p = lo
    n = 0
    for p in range(lo, hi - W + 1):
        if align is not None and (p - lo) % 4 != align:
            continue
        o, u1, u2 = struct.unpack_from('<III', raw, p)
        if require_uid_eq and u1 != u2:
            continue
        if u1 == 0:
            continue
        if require_marker and raw[p+W-1] != 0:
            continue
        out[o].append((p, u1))
        n += 1
    return out, n

def count_tilings(raw, header, footer, n, W, align=None, require_marker=False,
                  strict_uid=True, min_row=1, max_states=200000):
    end = len(raw) - footer
    cands, ncand = build_cands(raw, header, end, W, align, require_marker)
    layers = [cands.get(i, []) for i in range(n)]
    layers = [sorted(l) for l in layers]
    missing = [i for i, l in enumerate(layers) if not l]
    if missing:
        return 0, {'missing_layers': missing[:10], 'n_cand': ncand}
    # dp[i]: pos -> count, plus last uid for constraint => keep dict pos -> dict(uid->count)
    dp = [dict() for _ in range(n+1)]
    dp[0][header] = {0: 1}
    for i in range(n):
        nxt = {}
        for pos, uids in dp[i].items():
            for pk, uid in layers[i]:
                if pk < pos + min_row - W and pk < pos:
                    continue
                if pk < pos:
                    continue
                e = pk + W
                if e > end:
                    continue
                for lu, c in uids.items():
                    if strict_uid and uid <= lu:
                        continue
                    d = nxt.setdefault(e, {})
                    d[uid] = d.get(uid, 0) + c
        # prune
        tot = sum(sum(v.values()) for v in nxt.values())
        if tot == 0:
            return 0, {'broke_at': i, 'n_cand': ncand}
        # collapse: keep only minimal uid per pos (dominant state) if counts explode
        if len(nxt) > max_states:
            return None, {'overflow_at': i, 'states': len(nxt)}
        dp[i+1] = nxt
    final = dp[n].get(end, {})
    paths = sum(final.values())
    return paths, {'n_cand': ncand, 'states_last': len(dp[n])}

if __name__ == '__main__':
    tests = [('client',7,208),('server',7,208),('client',18,1567),('server',18,1567),
             ('client',27,334),('server',27,334),('client',8,126),('server',8,126),
             ('client',56,6),('server',56,6),('client',47,2488),('server',47,2488)]
    for arch,tid,n in tests:
        raw = load(arch,tid)
        for W,mk in ((13,True),(12,False)):
            for align in (0,1,2,3,None):
                for foot in (8,):
                    p,info = count_tilings(raw,14,foot,n,W,align,mk)
                    if p:
                        print(arch,tid,'W',W,'mk',mk,'align',align,'foot',foot,'-> paths',p,info)
        print()
