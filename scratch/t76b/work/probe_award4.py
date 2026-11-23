"""t76b scratch: award(0) — null-sentinel structure + FK membership + dependency correlation."""
import runpy, sys, struct, json
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()


def load(tid, arch="client"):
    return D["load_payload"](C, arch, tid)


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def var_rows(raw, n, lo, hi):
    """Backtrack one chain; returns [(start,end,uid)]."""
    from collections import defaultdict
    ways = [defaultdict(int) for _ in range(n + 1)]
    prev = defaultdict(list)
    ways[0][lo] = 1
    for j in range(n):
        for p in sorted(ways[j]):
            for e in range(p + 13, hi + 1):
                o, u1, u2, m = struct.unpack_from("<IIIB", raw, e - 13)
                if o == j and u1 == u2 != 0 and m == 0:
                    if e not in ways[j + 1]:
                        prev[(j + 1, e)].append(p)
                    ways[j + 1][e] += ways[j][p]
    ends = [e for e, w in ways[n].items() if w]
    if not ends:
        return None
    e = max(ends)
    out = []
    for j in range(n, 0, -1):
        ps = [p for p in prev[(j, e)] if ways[j - 1].get(p, 0)]
        if not ps:
            return None
        p = min(ps)
        out.append((p, e, u32(raw, e - 9)))
        e = p
    out.reverse()
    return out


# reference domains
cont = [1, 2, 3, 4, 5, 6, 7]
raw9 = load(9)
r9 = var_rows(raw9, u32(raw9, 8), 14, len(raw9) - 8)
nation = [r[2] for r in r9]
raw25 = load(25)
comp = [u32(raw25, 14 + j * 127 + 114 + 4) for j in range(7047)]
raw2 = load(2)
city = [u32(raw2, 14 + j * 43 + 30 + 4) for j in range(56293)]
raw21 = load(21)
stad = [u32(raw21, 14 + j * 38 + 25 + 4) for j in range(48413)]
print("nation n=%d sample=%s" % (len(nation), nation[:8]))
print("comp n=%d range=%s..%s" % (len(comp), min(comp), max(comp)))

raw = load(0)
H, S, n = 14, 77, 3545
rows = [raw[H + j * S:H + (j + 1) * S] for j in range(n)]

print("\n== u32 columns vs reference UID domains (allowing 0 and 0xffffffff as null) ==")
for off in range(0, 61):
    v = [u32(r, off) for r in rows]
    nn = [x for x in v if x not in (0, 0xFFFFFFFF)]
    if not nn:
        continue
    res = []
    for nm, dom in (("continent", cont), ("nation", nation), ("comp", comp),
                    ("city", city), ("stadium", stad)):
        ds = set(dom)
        h = sum(1 for x in nn if x in ds)
        if h == len(nn) and len(set(nn)) > 1:
            res.append(f"{nm}:ALL({len(set(nn))} vals)")
        elif h >= 0.9 * len(nn):
            res.append(f"{nm}:{h}/{len(nn)}")
    if res:
        print(f" off{off:2d} nulls0={v.count(0)} nullff={v.count(0xFFFFFFFF)} "
              f"set={len(set(nn))} range=({min(nn)},{max(nn)}) -> {res}")

print("\n== joint null structure off 23..34, 41..44 ==")
for base, w in ((23, 4), (27, 4), (31, 4), (41, 4), (44, 4)):
    pat = Counter()
    for r in rows:
        pat[r[base:base + w].hex()] += 1
    print(f" off{base} w{w}: {pat.most_common(6)}")

print("\n== dependency correlation: AWdr==6 -> AWda present ==")
for cand in (19, 60):
    yrs = [int.from_bytes(r[cand + 2:cand + 4], "little") for r in rows]
    setv = [y != 1900 for y in yrs]
    for other in (2, 20, 35, 46, 47, 49, 50, 51, 52, 55, 59, 61):
        vals = [r[other] for r in rows]
        for k in sorted(set(vals)):
            mask = [x == k for x in vals]
            cnt = sum(mask)
            if cnt < 20:
                continue
            hit = sum(1 for i in range(n) if mask[i] and setv[i])
            if hit / cnt > 0.9 and sum(setv) < cnt * 0.5:
                print(f"  date@{cand}: rows with byte{other}=={k} ({cnt}) -> date set {hit}/{cnt}")
