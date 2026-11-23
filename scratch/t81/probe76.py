"""t81-fix1 probe76 — 27B tiling budget + binary column identity pairs."""
import json
import runpy
from collections import Counter
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p76")
M = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text("utf-8"))
rs = core["load_payload"]("server", 6)
n = 115
col = lambda o, w=1: [int.from_bytes(rs[14 + j * 40 + o: 14 + j * 40 + o + w], "little")
                      for j in range(n)]

F = M["entities"]["injury.xml"][0]["fields"]
nonstr = [f for f in F if f["type"] != "string"]
print("non-string fields:", len(nonstr))
print("  counts:", Counter(f["type"] for f in nonstr))

# declared-width budget from min_value/max_value
def width_for(f):
    if f["type"] == "real":
        return 4
    if f["type"] in ("boolean", "enum"):
        return 1
    if f["type"] == "multiple_enum":
        return 2
    if f["type"] == "integer":
        hi = int(f.get("max_value", 2 ** 31 - 1))
        return 1 if hi <= 255 else (2 if hi <= 65535 else 4)
    return None

budget = {f["field"]: width_for(f) for f in nonstr}
print("  budget:", budget, "total =", sum(v for v in budget.values() if v))

print("\n--- observed slot widths (my tiling)")
tile = [(0, 1), (1, 1), (2, 1), (3, 2), (5, 2), (7, 1), (8, 1), (9, 1), (10, 1),
        (11, 1), (12, 1), (13, 4), (17, 1), (18, 2), (20, 1), (21, 1), (22, 1),
        (23, 1), (24, 1), (25, 1), (26, 1)]
print("  slots:", len(tile), "bytes:", sum(w for _, w in tile),
      "contiguous:", all(tile[i][0] + tile[i][1] == tile[i + 1][0] for i in range(len(tile) - 1)))
print("  u8 slots:", sum(1 for _, w in tile if w == 1),
      "u16:", sum(1 for _, w in tile if w == 2), "u32/f32:", sum(1 for _, w in tile if w == 4))

print("\n--- binary columns and their identity pairs")
bins = [o for o in range(27) if set(col(o)) <= {0, 1} and len(set(col(o))) == 2]
print("  non-constant binary:", bins)
for i, a in enumerate(bins):
    for b in bins[i + 1:]:
        if col(a) == col(b):
            print(f"   identical: off{a} == off{b}")
for a in bins:
    print(f"   off{a}: ones={sum(col(a))}/{n}")

print("\n--- ff-sentinel columns")
for o in range(27):
    c = col(o)
    if c.count(255) >= 1:
        print(f"  off{o}: ff={c.count(255)} live={[x for x in set(c) if x != 255][:8]}")
