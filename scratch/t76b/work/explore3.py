"""t76b scratch: identity-chain DP with backtracking (var tables)."""
import runpy, sys, struct
from pathlib import Path
from collections import defaultdict

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()


def load(tid, arch="client"):
    return D["load_payload"](C, arch, tid)


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def chains(raw, n, lo, hi, identity_width=13, ordinal=True):
    """All rows must end with [ord][uid][uid][marker]. Returns (ways_end, prev)."""
    ways = [defaultdict(int) for _ in range(n + 1)]
    prev = defaultdict(list)          # (j,e) -> [pos...]
    ways[0][lo] = 1
    for j in range(n):
        starts = sorted(ways[j])
        for p in starts:
            for e in range(p + identity_width, hi + 1):
                o, u1, u2, m = struct.unpack_from("<IIIB", raw, e - 13)
                ok = (u1 == u2 != 0 and m == 0) and (o == j if ordinal else True)
                if ok:
                    if e not in ways[j + 1]:
                        prev[(j + 1, e)].append(p)
                    ways[j + 1][e] += ways[j][p]
    return ways, prev


def chain_uids(raw, n, lo, hi, ordinal=True):
    ways, prev = chains(raw, n, lo, hi, ordinal=ordinal)
    ends = {e: w for e, w in ways[n].items()}
    if not ends:
        return None, "no chain to footer"
    best = max(ends, key=lambda e: (ends[e], e))
    rows = []
    e = best
    for j in range(n, 0, -1):
        ps = [p for p in prev[(j, e)] if ways[j - 1].get(p, 0)]
        if not ps:
            return None, f"backtrack broke at row {j} end {e}"
        p = min(ps)
        rows.append((p, e, u32(raw, e - 9), u32(raw, e - 5)))
        e = p
    rows.reverse()
    return rows, {"ends": sorted(ends), "ways": ends[best]}


if __name__ == "__main__":
    raw = load(10)
    n = u32(raw, 8)
    rows, info = chain_uids(raw, n, 14, len(raw) - 8)
    print("t10", info)
    print("uids", [r[2] for r in rows][:12], "n", len(rows))
    print("len_hist", {})
