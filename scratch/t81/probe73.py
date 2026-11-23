"""t81-fix1 probe73 — 27B tiling test: field/width budget vs observed columns."""
import itertools
import json
import runpy
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p73")
M = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text("utf-8"))
rs = core["load_payload"]("server", 6)
n = 115
col = lambda off, w: [int.from_bytes(rs[14 + j * 40 + off: 14 + j * 40 + off + w], "little")
                      for j in range(n)]

print("u16@18: min=%d max=%d d=%d" % (min(col(18, 2)), max(col(18, 2)), len(set(col(18, 2)))))
icau = {int(v["enum"]) for v in M["enums"]["Icau"]["values"] if int(v["enum"]) > 0}
masks = {0}
for k in range(1, len(icau) + 1):
    for c in itertools.combinations(sorted(icau), k):
        masks.add(sum(c))
v26 = set(col(26, 1))
v18 = set(col(18, 2))
print("off26 subset Icau masks:", v26 <= masks, "| off18 subset:", v18 <= masks)
print("off26 as bit positions:", sorted({bin(x) for x in v26})[:6])

print("\n--- {0,1} columns (u8) and const-0 columns")
b = [o for o in range(27) if set(col(o, 1)) <= {0, 1}]
z = [o for o in range(27) if set(col(o, 1)) == {0}]
print("  {0,1}:", b, " const0:", z)

print("\n--- declared boolean count / pct count / days count / enum count")
F = M["entities"]["injury.xml"][0]["fields"]
from collections import Counter
print("  types:", Counter(f["type"] for f in F))
print("  booleans:", [f["field"] for f in F if f["type"] == "boolean"])
print("  pct(0..100 ints):", [f["field"] for f in F
                              if f.get("min_value") == "0" and f.get("max_value") == "100"])
print("  days(0..720):", [f["field"] for f in F if f.get("max_value") == "720"])

print("\n--- u16 candidates at every even/odd offset with max<512")
for off in range(26):
    w = col(off, 2)
    if max(w) < 512 and min(w) >= 0:
        print(f"  u16@{off}: min={min(w)} max={max(w)} d={len(set(w))}")
