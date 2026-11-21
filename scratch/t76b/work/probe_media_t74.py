"""t76b scratch: media rows at t74 boundaries + mid grammar; award date gating set equality."""
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


def media_rows(arch, expect_first):
    """Walk with the documented grammar; pick the *last* valid trailer before next name."""
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
        if best is None:
            return raw, rows, f"row {j} at {pos}: no trailer"
        rows.append((pos, best))
        pos = best
    return raw, rows, (None if pos == hi else f"ended {pos} != {hi}")


for arch, exp in (("client", 190), ("server", 197)):
    raw, rows, err = media_rows(arch, exp)
    print(f"=== media {arch}: rows={len(rows)} err={err} first_len="
          f"{rows[0][1] - rows[0][0] if rows else None} (t74 says {exp})")
    lens = [e - s for s, e in rows]
    print("   lens range", min(lens), max(lens), "sum", sum(lens),
          "payload", len(raw), "close", sum(lens) + 14 + 8 == len(raw))
    bad = []
    shapes = Counter()
    for j, (s, e) in enumerate(rows):
        body = raw[s:e]
        k = u32(body, 0)
        ul = u32(body, 10 + k)
        a = 14 + k + ul
        mid = body[a:len(body) - 18]
        if len(mid) < 34:
            shapes["short"] += 1
            continue
        cnt = u32(mid, 30)
        if len(mid) == 34 + 12 * cnt:
            trip = [struct.unpack_from("<III", mid, 34 + 12 * i) for i in range(cnt)]
            okp = all(x == y for x, y, z in trip)
            okz = all(z == 0 for x, y, z in trip)
            shapes[f"34+12*{cnt} paireq={okp} z0={okz}"] += 1
        elif len(mid) == 34 + 12 * u32(mid, 30) + 7:
            shapes["34+12n+7"] += 1
        else:
            bad.append((j, len(mid)))
    print("   mid shapes:", shapes.most_common(8))
    print("   bad mid:", bad[:5], len(bad))
