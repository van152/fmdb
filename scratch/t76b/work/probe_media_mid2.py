"""t76b scratch: media(7) middle hypothesis test: [2B][8x u32, last=count][count x 12B triples]."""
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
                if e == hi or u32(raw, e) <= 64:
                    break
        rows.append((pos, e))
        pos = e
    return raw, rows


for arch in ("client", "server"):
    raw, rows = walk(arch)
    ok = Counter()
    hdr = Counter()
    samples = []
    for j, (s, e) in enumerate(rows):
        body = raw[s:e]
        k = u32(body, 0)
        six = body[4 + k:10 + k]
        ul = u32(body, 10 + k)
        a = 14 + k + ul
        L = len(body)
        # find the 5B prefix + 13B trailer at the end
        mid_end = L - 18
        mid = body[a:mid_end]
        if len(mid) >= 34:
            cnt = u32(mid, 32)
            if len(mid) == 34 + 12 * cnt:
                trip = [struct.unpack_from("<III", mid, 34 + 12 * i) for i in range(cnt)]
                paireq = sum(1 for x, y, z in trip if x == y)
                z0 = sum(1 for x, y, z in trip if z == 0)
                ok[("len-ok", cnt == 0 or paireq == cnt, cnt == 0 or z0 == cnt)] += 1
                hdr[(u32(mid, 0), u32(mid, 4), u32(mid, 8), u32(mid, 12),
                     u32(mid, 16), u32(mid, 20), u32(mid, 24), cnt)] += 1
            else:
                ok[("len-mismatch", None, None)] += 1
        else:
            ok[("short", None, None)] += 1
    print(f"=== {arch}: {dict(ok)}")
    print("  hdr shapes (8 u32 with last=count):")
    for kk, v in hdr.most_common(8):
        print("   ", kk, v)
