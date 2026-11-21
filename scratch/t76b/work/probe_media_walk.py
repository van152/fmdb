"""t76b scratch: media(7) grammar-first walker (name-len prefix + identity trailer)."""
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


def valid_name(b):
    try:
        s = b.decode("utf-8")
    except UnicodeDecodeError:
        return None
    if not s or len(s) > 64:
        return None
    if any(ord(c) < 0x20 for c in s):
        return None
    return s


def walk(arch):
    raw = load(7, arch)
    n = u32(raw, 8)
    hi = len(raw) - 8
    pos, rows, probs = 14, [], []
    for j in range(n):
        k = u32(raw, pos)
        if k > 64:
            probs.append((j, pos, "name_len", k))
            break
        nm = valid_name(raw[pos + 4:pos + 4 + k])
        if nm is None:
            probs.append((j, pos, "name_utf8", raw[pos + 4:pos + 4 + k].hex()))
            break
        # find the identity trailer for this row: search forward for a valid one
        cand = []
        for e in range(pos + 13 + 4 + k, hi + 1):
            o, u1, u2, m = struct.unpack_from("<IIIB", raw, e - 13)
            if o == j and u1 == u2 != 0 and m == 0:
                # next row must start with a readable name-len prefix (or be the footer)
                nxt = raw[e:e + 4]
                if e == hi:
                    cand.append(e)
                else:
                    k2 = u32(raw, e)
                    if k2 <= 64 and valid_name(raw[e + 4:e + 4 + k2]) is not None:
                        cand.append(e)
        if not cand:
            probs.append((j, pos, "no_trailer", None))
            break
        e = cand[0]
        rows.append({"j": j, "start": pos, "end": e, "name": nm, "k": k,
                     "ncand": len(cand)})
        pos = e
    return raw, n, rows, probs, pos


for arch in ("client", "server"):
    raw, n, rows, probs, pos = walk(arch)
    print(f"=== {arch} n={n} rows={len(rows)} end={pos} payload={len(raw)} "
          f"footer={len(raw) - pos} probs={probs[:3]}")
    print("   ncand hist:", Counter(r["ncand"] for r in rows))
    print("   len range:", min(r["end"] - r["start"] for r in rows),
          max(r["end"] - r["start"] for r in rows))
