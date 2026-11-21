"""t76b scratch: final probes — media 6B count correlation, client/server relations."""
import runpy, sys, struct, hashlib, json
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


# ---- 1. award client vs server ----
for arch in ("client", "server"):
    raw = D["load_payload"](C, arch, 0)
    n = u32(raw, 8)
    print(f"award {arch}: payload={len(raw)} n={n} stride={(len(raw)-22)//n} "
          f"sha={hashlib.sha256(raw).hexdigest()[:16]}")

# ---- 2. language client vs server ----
for arch in ("client", "server"):
    raw = D["load_payload"](C, arch, 8)
    print(f"language {arch}: payload={len(raw)} sha={hashlib.sha256(raw).hexdigest()[:16]}")


# ---- media walker ----
def media_rows(arch):
    raw = D["load_payload"](C, arch, 7)
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


def parts(arch, j):
    raw, rows = media_rows(arch)
    s, e = rows[j]
    body = raw[s:e]
    k = u32(body, 0)
    ul = u32(body, 10 + k)
    return {"name": body[4:4 + k], "six": body[4 + k:10 + k], "url": body[14 + k:14 + k + ul],
            "mid": body[14 + k + ul:len(body) - 18], "pre5": body[len(body) - 18:len(body) - 13],
            "ident": body[len(body) - 13:], "body": body}


print("\n== media 6B: u16@4 (big-endian read) vs mid candidate counts ==")
for arch in ("client", "server"):
    raw, rows = media_rows(arch)
    agree = Counter()
    for j, (s, e) in enumerate(rows):
        p = parts(arch, j)
        six = p["six"]
        b0, b1, b2, b3, b4, b5 = six
        v = (b4 << 8) | b5          # big-endian last u16
        mid = p["mid"]
        cands = []
        for H in range(0, min(len(mid) - 3, 70)):
            c = u32(mid, H)
            if c > 4096:
                continue
            if H + 4 + 12 * c == len(mid) or 34 + 12 * c == len(mid):
                cands.append(c)
        agree[(v, tuple(cands))] += 1
    hit = sum(c for (v, cs), c in agree.items() if v in cs)
    print(f"  {arch}: 6B-u16@4 == a valid mid count on {hit}/{len(rows)} rows")
    print(f"    top pairs: {agree.most_common(5)}")

print("\n== media client vs server: row-by-row delta ==")
rc, rws_c = media_rows("client")
rs, rws_s = media_rows("server")
deltas = Counter()
for j in range(len(rws_c)):
    pc, ps = parts("client", j), parts("server", j)
    deltas[(len(ps["mid"]) - len(pc["mid"]),
            len(ps["name"]) - len(pc["name"]),
            len(ps["url"]) - len(pc["url"]),
            ps["six"] == pc["six"], ps["pre5"] == pc["pre5"])] += 1
print("  (mid_d, name_d, url_d, six_eq, pre5_eq) ->", deltas.most_common(6))
print("  example row0 client mid:", parts("client", 0)["mid"].hex())
print("  example row0 server mid:", parts("server", 0)["mid"].hex())
