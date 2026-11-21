"""t76b scratch: media(7) middle-region structural scan (count-prefixed 12B triples)."""
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


def walk(arch):
    raw = load(7, arch)
    n = u32(raw, 8)
    hi = len(raw) - 8
    pos, rows = 14, []
    for j in range(n):
        k = u32(raw, pos)
        for e in range(pos + 13 + 4 + k, hi + 1):
            o, u1, u2, m = struct.unpack_from("<IIIB", raw, e - 13)
            if o == j and u1 == u2 != 0 and m == 0:
                if e == hi or (u32(raw, e) <= 64):
                    break
        rows.append((pos, e))
        pos = e
    return raw, rows


raw, rows = walk("client")
print("rows", len(rows))
pre_hist = Counter()
triple_ok = Counter()
for j, (s, e) in enumerate(rows):
    body = raw[s:e]
    k = u32(body, 0)
    six = body[4 + k:10 + k]
    ul = u32(body, 10 + k)
    a = 14 + k + ul
    trailer = e - 18                     # 5B prefix + 13B trailer
    found = None
    for p in range(a, trailer - 3):
        c = u32(body, p)
        if c > 4096:
            continue
        rest = trailer - (p + 4)
        if rest == 12 * c:
            items = [struct.unpack_from("<III", body, p + 4 + 12 * i) for i in range(c)]
            found = (p, c, sum(1 for x, y, z in items if x == y),
                     sum(1 for x, y, z in items if z == 0))
            break
    pre_hist[(found[0] - a) if found else None] += 1
    if found:
        triple_ok[(found[1] > 0, found[2] == found[1], found[3] == found[1])] += 1
print("pre-block sizes:", pre_hist.most_common(10))
print("triple shape (count>0, a==b all, z==0 all):", triple_ok)
