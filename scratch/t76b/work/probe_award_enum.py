"""t76b scratch: award(0) enum-domain matching + AWdr/AWda gate recovery."""
import runpy, sys, struct, json
from pathlib import Path
from collections import Counter, defaultdict

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()
REPO = Path(r"D:/tmp2b/fm24-db")
S = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text(encoding="utf-8"))
EN = S["enums"]
ENT = S["entities"]


def enum_ids(name):
    e = EN.get(name)
    if not e:
        return None
    out = []
    for v in e["values"]:
        try:
            out.append(int(v["enum"]))
        except (TypeError, ValueError):
            pass
    return set(out)


AW_ENUMS = {f["field"]: enum_ids(f.get("enum_ref") or f["field"])
            for f in ENT["award.xml"][0]["fields"] if f["type"] == "enum"}
print("award enum domains:")
for k, v in AW_ENUMS.items():
    print(f"  {k:5s} n={len(v):3d} {sorted(v)[:20] if v else v}")

arch = "client"
raw = D["load_payload"](C, arch, 0)
n = struct.unpack_from("<I", raw, 8)[0]
S77 = (len(raw) - 22) // n
rows = [raw[14 + j * S77:14 + (j + 1) * S77] for j in range(n)]
biz = [r[:64] for r in rows]
print(f"\n{arch} rows={n} stride={S77} biz=64B")

print("\n== u8 column vs enum domains (exact ==, or subset with full coverage) ==")
for o in range(64):
    v = {r[o] for r in rows}
    if len(v) == 1 or len(v) > 40:
        continue
    hits = []
    for f, d in AW_ENUMS.items():
        if not d:
            continue
        if v == d:
            hits.append((f, "EXACT"))
        elif v <= d and len(v) >= max(3, 0.5 * len(d)):
            hits.append((f, "subset"))
    if hits:
        print(f"  b{o:2d} d={len(v):3d} {sorted(v)} -> {hits}")

print("\n== gating: which column's value predicts date@19 presence ==")
d19 = [int.from_bytes(r[19:21], "little") != 1 or
       int.from_bytes(r[21:23], "little") != 1900 for r in rows]
d60 = [int.from_bytes(r[60:62], "little") != 1 or
       int.from_bytes(r[62:64], "little") != 1900 for r in rows]
print(f"  date@19 set: {sum(d19)}  date@60 set: {sum(d60)}")
for o in range(64):
    v = [r[o] for r in rows]
    if len(set(v)) > 12:
        continue
    for val in sorted(set(v)):
        m = [x == val for x in v]
        c19 = sum(1 for a, b in zip(m, d19) if a and b)
        t19 = sum(m)
        if t19 and c19 == t19:
            print(f"  b{o:2d}=={val}: {t19:4d} rows -> date@19 set {c19}/{t19} (100%)")
        c60 = sum(1 for a, b in zip(m, d60) if a and b)
        if t19 and c60 == t19:
            print(f"  b{o:2d}=={val}: {t19:4d} rows -> date@60 set {c60}/{t19} (100%)")
