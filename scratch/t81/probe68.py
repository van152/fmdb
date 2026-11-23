"""t81-fix1 probe68 — enum exact-match search, f32 ratio test, other_records."""
import json
import runpy
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p68")
M = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text("utf-8"))
E = {}
for nm, rec in M["enums"].items():
    s = {int(v["enum"]) for v in rec.get("values", []) if str(v["enum"]).lstrip("-").isdigit()}
    if s:
        E[nm] = s

raw_c = core["load_payload"]("client", 6)
n = 115
col0 = {raw_c[14 + j * 16] for j in range(n)}
print("col0 =", sorted(col0))
print("exact:", [k for k, v in E.items() if v == col0])
print("minus(-3) exact:", [k for k, v in E.items() if v - {-3} == col0])
print("superset, |set|<=20:", [(k, sorted(v)) for k, v in E.items() if col0 <= v and len(v) <= 20])

print("\n--- f32 ratio test (all rows, 1e-6<|x|<1e3, >=2 distinct) on server 6")
raw_s = core["load_payload"]("server", 6)
for off in range(24):
    f = [struct.unpack_from("<f", raw_s, 14 + j * 40 + off)[0] for j in range(n)]
    if all(x == x and 1e-6 < abs(x) < 1e3 or x == 0 for x in f) and len(set(f)) >= 2:
        print(f"  off{off:2d} distinct={len(set(f))} min={min(f)} max={max(f)}")

print("\n--- other_records")
for xml in ("stage name.xml", "description.xml"):
    print(" ", xml, json.dumps(M["entities"][xml][0].get("other_records"), ensure_ascii=False)[:400])
