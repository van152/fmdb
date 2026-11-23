"""t76b scratch: wrong-UID control — small-integer coincidence test."""
import runpy, sys, struct, json
from pathlib import Path
from collections import defaultdict, Counter

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()


def load(tid, arch="client"):
    return D["load_payload"](C, arch, tid)


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def fixed_uids(tid, H, S, off):
    raw = load(tid)
    n = (len(raw) - H - 8) // S
    return [u32(raw, H + j * S + off + 4) for j in range(n)]


def var_uids(tid):
    raw = load(tid)
    n = u32(raw, 8)
    hi = len(raw) - 8
    ways = [defaultdict(int) for _ in range(n + 1)]
    prev = defaultdict(list)
    ways[0][14] = 1
    for j in range(n):
        for p in sorted(ways[j]):
            for e in range(p + 13, hi + 1):
                o, u1, u2, m = struct.unpack_from("<IIIB", raw, e - 13)
                if o == j and u1 == u2 != 0 and m == 0:
                    if e not in ways[j + 1]:
                        prev[(j + 1, e)].append(p)
                    ways[j + 1][e] += ways[j][p]
    ends = [e for e in ways[n] if ways[n][e]]
    e = max(ends)
    out = []
    for j in range(n, 0, -1):
        ps = [p for p in prev[(j, e)] if ways[j - 1].get(p, 0)]
        p = min(ps)
        out.append((u32(raw, e - 9), u32(raw, p)))
        e = p
    out.reverse()
    return out


dom = {
    "continent(t5)": fixed_uids(5, 14, 34, 21),
    "city(t2)": fixed_uids(2, 14, 43, 30),
    "comp(t25)": fixed_uids(25, 14, 127, 114),
    "stadium(t21)": fixed_uids(21, 14, 38, 25),
    "region(t19)": fixed_uids(19, 14, 45, 32),
    "nation(t10)": [x[0] for x in var_uids(10)],
}
print("reference domains: density of the low range")
for nm, v in dom.items():
    s = set(v)
    low = sorted(x for x in s if x <= 300)
    print(f"  {nm}: n={len(s)} max={max(s)} | ≤300: {len(low)} "
          f"{low[:14]}{'...' if len(low) > 14 else ''}")

print("\nnull-rate of a *uniform* integer probe against each domain, sizes 248/130/530")
for nm, v in dom.items():
    s = set(v)
    for hi in (5, 130, 250, 530):
        fake = list(range(1, hi + 1))
        hit = sum(1 for x in fake if x in s) / len(fake)
        print(f"  {nm:16} uniform 1..{hi:4d} -> hit {hit:.4f}")
    print()
