"""t81-fix1 probe77 — final enum containment sweep over all 304 master enums."""
import json
import runpy
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p77")
M = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text("utf-8"))
E = {}
for nm, rec in M["enums"].items():
    s = {int(v["enum"]) for v in rec.get("values", []) if str(v["enum"]).lstrip("-").isdigit()}
    if s:
        E[nm] = s
print("enums with ints:", len(E))

for tid, arc, H, S, biz in ((6, "server", 14, 40, 27), (6, "client", 14, 16, 3)):
    raw = core["load_payload"](arc, tid)
    n = 115
    print(f"\n===== {arc}/{tid}")
    for off in range(biz):
        col = {raw[H + j * S + off] for j in range(n)}
        exact = [k for k, v in E.items() if v == col]
        # subset only within injury's own enums (scoped test)
        scoped = [k for k in ("icla", "iscl", "inSr", "Iagr", "Icms")
                  if col <= E[k]]
        tight = [(k, len(E[k])) for k in scoped if len(E[k]) <= 2 * max(1, len(col)) + 4]
        print(f"  off{off:2d} d={len(col):2d} exact={exact} scoped_subset={scoped} tight={tight}")
