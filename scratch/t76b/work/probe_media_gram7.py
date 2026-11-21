"""t76b scratch: media(7) mid = HDR + u32 count + count x (u32,u32,u32 urllen,URL)."""
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


def parse_mid(mid):
    """Return (H, count, items) if exactly one H closes the byte stream."""
    hits = []
    for H in range(0, min(64, len(mid))):
        if H + 4 > len(mid):
            break
        cnt = u32(mid, H)
        if cnt > 4096:
            continue
        p = H + 4
        items = []
        ok = True
        for _ in range(cnt):
            if p + 12 > len(mid):
                ok = False
                break
            a, b, ln = struct.unpack_from("<III", mid, p)
            p += 12
            if p + ln > len(mid):
                ok = False
                break
            items.append((a, b, ln, mid[p:p + ln]))
            p += ln
        if ok and p == len(mid):
            hits.append((H, cnt, items))
    return hits


for arch in ("client", "server"):
    raw, rows = media_rows(arch)
    print(f"=== {arch}")
    hs = Counter()
    mult = Counter()
    bad = []
    shapes = Counter()
    for j, (s, e) in enumerate(rows):
        body = raw[s:e]
        k = u32(body, 0)
        ul = u32(body, 10 + k)
        a = 14 + k + ul
        mid = body[a:len(body) - 18]
        hits = parse_mid(mid)
        mult[len(hits)] += 1
        if len(hits) == 1:
            H, cnt, items = hits[0]
            hs[H] += 1
            shapes[(all(x == y for x, y, _, _ in items), cnt)] += 1
        else:
            bad.append((j, len(mid), len(hits)))
    print("  #distinct closures per row:", dict(mult))
    print("  H hist:", hs.most_common(8))
    print("  bad rows:", bad[:8], "n=", len(bad))
    print("  (a==b for all items, count):", shapes.most_common(6))
