"""Exploration: layered identity-triple DP tiling."""
import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct

def cand(raw, lo, hi, width=12, marker=False, align=None):
    """Yield (end_pos, ordinal, uid1, uid2) for every position where a 12B identity
    triple ends at end_pos and satisfies uid1==uid2, uid>0, ordinal>=0."""
    out=[]
    for p in range(lo, hi-width+1):
        if align is not None and (p % 4) != align:
            continue
        o,u1,u2 = struct.unpack_from('<III', raw, p)
        if u1 != u2 or u1 == 0:
            continue
        if marker and raw[p+12] != 0:
            continue
        out.append((p+width, o, u1))
    return out

def tile(raw, header, footer, n, width=12, marker=False, align=None,
         strict_uid=True, name_first=False):
    end = len(raw)-footer
    cs = cand(raw, header, end, width, marker, align)
    by_ord = {}
    for e,o,u in cs:
        by_ord.setdefault(o, []).append((e,u))
    for k in by_ord: by_ord[k].sort()
    if not all(k in by_ord for k in range(n)):
        return None, {k: len(by_ord.get(k,[])) for k in range(n) if k not in by_ord}
    # layered DP: state (end_pos, last_uid) -> count, but we just need reachability+count
    # layer 0: row0 start == header
    start = header
    cur = {start: [0]}  # end_pos -> list of last uid (keep minimal?)
    # simpler: DP over dp[i] = dict end_pos -> list of lastuid
    dp = [dict() for _ in range(n+1)]
    dp[0][header] = [0]
    for i in range(n):
        nxt = {}
        for pos, uids in dp[i].items():
            for e,u in by_ord.get(i, []):
                if e - width < pos:  # row is [pos, e)
                    continue
                if e - width == pos or e-width > pos:
                    if e-width != pos: continue
                good = [lu for lu in uids if (not strict_uid) or u > lu]
                if not good: continue
                nxt.setdefault(e, []).extend([u]) if u not in nxt.get(e,[]) else None
        dp[i+1] = nxt
        if not nxt: return 0, f"layer {i} empty"
    return (1 if end in dp[n] else 0), {i: len(dp[i]) for i in range(n+1)}

if __name__ == '__main__':
    tests = [('client',7,208),('server',7,208),('client',18,1567),('server',18,1567),
             ('client',27,334),('server',27,334),('client',8,126),('server',8,126)]
    for arch,tid,n in tests:
        raw = load(arch,tid)
        for width,marker in ((12,False),(13,True)):
            for align in (None,0,1,2,3):
                ok, info = tile(raw,14,8,n,width,marker,align)
                print(arch,tid,'w',width,'mk',marker,'align',align,'->',ok, str(info)[:90])
        print()
