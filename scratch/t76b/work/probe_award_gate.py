"""t76b scratch: award(0) dependency-gated set equality (AWdr==6 -> AWda)."""
import runpy, sys, struct, json
from pathlib import Path
from collections import Counter

sys.path.insert(0, str(Path(r"D:/tmp2b/fm24-db/scripts")))
D = runpy.run_path(r"D:/tmp2b/fm24-db/scripts/fm24_dump.py", run_name="x")
C = D["_reader"]()
REPO = Path(r"D:/tmp2b/fm24-db")
SCH = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text(encoding="utf-8"))
ENT = SCH["entities"]

FIELDS = ENT["award.xml"][0]["fields"]
print("== full dependency map (award) ==")
for f in FIELDS:
    deps = f.get("dependencies")
    if deps:
        print(f"  {f['field']:5s} {f['type']:8s} <- {json.dumps(deps)}")

raw = D["load_payload"](C, "client", 0)
n = struct.unpack_from("<I", raw, 8)[0]
S = (len(raw) - 22) // n
rows = [raw[14 + j * S:14 + (j + 1) * S] for j in range(n)]


def col(o, w):
    return [int.from_bytes(r[o:o + w], "little") for r in rows]


D19 = {j for j, r in enumerate(rows)
       if (int.from_bytes(r[19:21], "little"), int.from_bytes(r[21:23], "little")) != (1, 1900)}
D60 = {j for j, r in enumerate(rows)
       if (int.from_bytes(r[60:62], "little"), int.from_bytes(r[62:64], "little")) != (1, 1900)}
print(f"\ndate@19 rows={len(D19)} date@60 rows={len(D60)} overlap={len(D19 & D60)}")

print("\n== which (col,value) rowset EXACTLY equals date@19 or date@60 rowset? ==")
for o in range(64):
    v = col(o, 1)
    if len(set(v)) > 12:
        continue
    for val in sorted(set(v)):
        rs = {j for j, x in enumerate(v) if x == val}
        if rs == D19:
            print(f"  b{o:2d}=={val}: ==date@19  ({len(rs)} rows)")
        if rs == D60:
            print(f"  b{o:2d}=={val}: ==date@60  ({len(rs)} rows)")
for o in range(0, 61):
    v = col(o, 4)
    if len(set(v)) > 12:
        continue
    for val in sorted(set(v)):
        rs = {j for j, x in enumerate(v) if x == val}
        if rs == D19:
            print(f"  u32@{o:2d}=={val}: ==date@19  ({len(rs)} rows)")
        if rs == D60:
            print(f"  u32@{o:2d}=={val}: ==date@60  ({len(rs)} rows)")

print("\n== AWdr==6 candidate columns: rows where col==6 ==")
for o in range(64):
    v = col(o, 1)
    if 6 not in set(v):
        continue
    rs = {j for j, x in enumerate(v) if x == 6}
    print(f"  b{o:2d}==6 -> {len(rs)} rows | subset_of_d19={rs <= D19} "
          f"subset_of_d60={rs <= D60} | d19_in_rs={len(rs & D19)} d60_in_rs={len(rs & D60)}")

print("\n== b39/b40 (0..200 pair) zero counts and equality ==")
b39, b40 = col(39, 1), col(40, 1)
print("  b39 zeros", b39.count(0), "b40 zeros", b40.count(0),
      "equal_rows", sum(1 for a, b in zip(b39, b40) if a == b))
print("\n== b15 (0..20) vs AWre ==")
b15 = col(15, 1)
print("  min", min(b15), "max", max(b15), "distinct", len(set(b15)), "hist",
      sorted(Counter(b15).items())[:8])
