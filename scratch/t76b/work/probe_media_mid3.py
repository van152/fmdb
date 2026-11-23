"""t76b scratch: media(7) mid region — exact header layout + count-triples test."""
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
    print(f"=== {arch}")
    for j in (0, 1):
        s, e = rows[j]
        body = raw[s:e]
        k = u32(body, 0)
        ul = u32(body, 10 + k)
        a = 14 + k + ul
        L = len(body)
        mid = body[a:L - 18]
        print(f" row{j} L={L} url_end={a} mid_len={len(mid)}")
        print("   mid hex:", mid.hex())
        for p in range(0, min(len(mid), 40), 4):
            print(f"     mid+{p:2d} u32={u32(mid, p) if p + 4 <= len(mid) else None}")
    # hypothesis: mid = HDR + u32 count + count x 12B ; HDR size unknown -> solve
    print("  solving HDR size per row (len(mid)-HDR-4 == 12*count at HDR):")
    hdr_sizes = Counter()
    fails = []
    for j, (s, e) in enumerate(rows):
        body = raw[s:e]
        k = u32(body, 0)
        ul = u32(body, 10 + k)
        a = 14 + k + ul
        mid = body[a:len(body) - 18]
        hit = None
        for H in range(0, 60):
            if H + 4 > len(mid):
                break
            c = u32(mid, H)
            if len(mid) == H + 4 + 12 * c:
                hit = (H, c)
                break
        if hit:
            hdr_sizes[hit[0]] += 1
        else:
            fails.append((j, len(mid)))
    print("   HDR size hist:", hdr_sizes.most_common())
    print("   fails:", fails[:6], "n", len(fails))
