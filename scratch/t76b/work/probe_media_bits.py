"""t76b scratch: media(7) 6B prefix bit-field scan vs Mper/Mscp/Msty + mid triple domains."""
import runpy, sys, struct, json
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()
SCH = json.loads((Path(r"D:/tmp2b/fm24-db/evidence/fm24/reports/editor_schema/master.json")
                  ).read_text(encoding="utf-8"))
EN, ENT = SCH["enums"], SCH["entities"]

NROWS = {"club": 84259, "comp": 7047, "stadium": 48413, "city": 56293,
         "nation": 251, "region": 28, "continent": 7, "language": 126,
         "media_source": 208, "local_region": 2488}


def u32(b, o):
    return struct.unpack_from("<I", b, o)[0]


def ids(name):
    out = set()
    for v in EN[name]["values"]:
        try:
            out.add(int(v["enum"]))
        except (TypeError, ValueError):
            pass
    return out


MED = {f["field"]: ids(f.get("enum_ref") or f["field"])
       for f in ENT["media source.xml"][0]["fields"] if f["type"] == "enum"}
print("media enums:", {k: (len(v), sorted(v)) for k, v in MED.items()})


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


for arch in ("client", "server"):
    raw, rows = media_rows(arch)
    print(f"\n=== media {arch} rows={len(rows)}")
    six6 = []
    for j, (s, e) in enumerate(rows):
        body = raw[s:e]
        k = u32(body, 0)
        six6.append(body[4 + k:10 + k])
    print("  distinct 6B prefixes:", len({x for x in six6}), Counter(six6).most_common(4))
    ints = [int.from_bytes(x, "little") for x in six6]
    print("  bit-field scan (6B, w=1..8):")
    for w in range(1, 9):
        mask = (1 << w) - 1
        for bit in range(0, 48 - w + 1):
            vals = {(x >> bit) & mask for x in ints}
            if len(vals) < 2 or len(vals) > 16:
                continue
            for f, d in MED.items():
                if d and vals <= d and len(vals) / len(d) >= 0.5:
                    print(f"    bit={bit:2d} w={w} {f} obs={len(vals)}/{len(d)} "
                          f"vals={sorted(vals)}")
    # mid triple domains
    tv = []
    for j, (s, e) in enumerate(rows):
        body = raw[s:e]
        k = u32(body, 0)
        ul = u32(body, 10 + k)
        mid = body[14 + k + ul:len(body) - 18]
        for H in range(len(mid) - 4):
            c = u32(mid, H)
            if 34 + 12 * c == len(mid) or H + 4 + 12 * c == len(mid):
                for i in range(c):
                    a, b, z = struct.unpack_from("<III", mid, H + 4 + 12 * i)
                    tv.append(a)
                break
    if tv:
        print(f"  mid triple first-values: n={len(tv)} min={min(tv)} max={max(tv)}")
        for t, N in NROWS.items():
            r = sum(1 for x in tv if x < N) / len(tv)
            if r > 0.95:
                print(f"    all-under {t}({N}): {r:.3f}")
