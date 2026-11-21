"""t76b scratch: media(7) full mid grammar validation, both archives."""
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


def media_rows(arch):
    raw = load(7, arch)
    n = u32(raw, 8)
    hi = len(raw) - 8
    pos, rows = 14, []
    for j in range(n):
        k = u32(raw, pos)
        best = None
        for e in range(pos + 13 + 4 + k, hi + 1):
            o, u1, u2, m = struct.unpack_from("<IIIB", raw, e - 13)
            if o != j or u1 != u2 or u1 == 0 or m != 0:
                continue
            if e < hi:
                k2 = u32(raw, e)
                if k2 > 64:
                    continue
                try:
                    nm = raw[e + 4:e + 4 + k2].decode("utf-8")
                except UnicodeDecodeError:
                    continue
                if not nm or any(ord(c) < 0x20 for c in nm):
                    continue
            best = e
        rows.append((pos, best))
        pos = best
    return raw, rows


for arch in ("client", "server"):
    raw, rows = media_rows(arch)
    print(f"=== {arch}")
    res = Counter()
    fails = []
    hdrs = []
    for j, (s, e) in enumerate(rows):
        body = raw[s:e]
        k = u32(body, 0)
        ul = u32(body, 10 + k)
        a = 14 + k + ul
        mid = body[a:len(body) - 18]
        if len(mid) < 34:
            res["mid<34"] += 1
            fails.append((j, len(mid), "short"))
            continue
        cnt = u32(mid, 30)
        exp = 34 + 12 * cnt
        if len(mid) == exp:
            trip = [struct.unpack_from("<III", mid, 34 + 12 * i) for i in range(cnt)]
            if all(x == y and z == 0 for x, y, z in trip):
                res["grammar_ok"] += 1
                hdrs.append(tuple(struct.unpack_from("<8I", mid, 0)))
            else:
                res["triple_shape_bad"] += 1
                fails.append((j, len(mid), "triple", trip[:3]))
        else:
            res["len_mismatch"] += 1
            fails.append((j, len(mid), cnt, exp))
    print("  ", dict(res))
    print("   fails:", fails[:6])
    print("   header tuples:", Counter(hdrs).most_common(6))
