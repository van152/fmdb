"""t76b scratch: media(7) middle-region grammar test."""
import runpy, sys, struct
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()


def load(tid, arch="client"):
    return D["load_payload"](C, arch, tid)


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def rows7(arch):
    raw = load(7, arch)
    n = u32(raw, 8)
    # DP identity chain, rows end with 13B trailer; row start = previous end
    from collections import defaultdict
    ways = [defaultdict(int) for _ in range(n + 1)]
    prev = defaultdict(list)
    ways[0][14] = 1
    hi = len(raw) - 8
    for j in range(n):
        for p in sorted(ways[j]):
            for e in range(p + 13, hi + 1):
                o, u1, u2, m = struct.unpack_from("<IIIB", raw, e - 13)
                if o == j and u1 == u2 != 0 and m == 0:
                    if e not in ways[j + 1]:
                        prev[(j + 1, e)].append(p)
                    ways[j + 1][e] += ways[j][p]
    ends = [e for e, w in ways[n].items() if w]
    assert len(ends) == 1, ends
    e = ends[0]
    out = []
    for j in range(n, 0, -1):
        ps = [p for p in prev[(j, e)] if ways[j - 1].get(p, 0)]
        assert ps, (j, e)
        p = min(ps)
        out.append((p, e))
        e = p
    out.reverse()
    return raw, out


for arch in ("client", "server"):
    raw, rows = rows7(arch)
    print(f"=== {arch}: {len(rows)} rows, payload {len(raw)}")
    stats = Counter()
    bad = []
    for j, (s, e) in enumerate(rows):
        body = raw[s:e]
        k = u32(body, 0)
        nm = body[4:4 + k]
        six = body[4 + k:10 + k]
        ul = u32(body, 10 + k)
        url = body[14 + k:14 + k + ul]
        mid_start = 14 + k + ul
        mid = body[mid_start:e - 18]          # 5B prefix + 13B trailer removed
        tag = None
        if len(mid) >= 34:
            nn = u32(mid, 30)
            if len(mid) == 34 + 12 * nn:
                items = [struct.unpack_from("<III", mid, 34 + 12 * i) for i in range(nn)]
                paired = sum(1 for a, b, c in items if a == b)
                zero3 = sum(1 for a, b, c in items if c == 0)
                tag = ("A", nn, paired, zero3)
        if tag is None:
            tag = ("?", len(mid))
            bad.append((j, len(mid), mid[:40].hex()))
        stats[tag[0]] += 1
    print("  tag counts:", stats)
    print("  bad sample:", bad[:5], "n_bad", len(bad))
