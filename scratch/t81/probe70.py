"""t81-fix1 probe70 — hierarchy test icla/iscl + raw enum file inspection."""
import json
import runpy
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p70")
M = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text("utf-8"))

print("--- icla enum file:", M["enums"]["icla"].get("file"))
print("--- icla raw values:")
for v in M["enums"]["icla"]["values"]:
    print("   ", json.dumps(v, ensure_ascii=False))
print("--- iscl file:", M["enums"]["iscl"].get("file"), "n=", len(M["enums"]["iscl"]["values"]))

rc = core["load_payload"]("client", 6)
n = 115
pairs = [(rc[14 + j * 16], rc[14 + j * 16 + 1]) for j in range(n)]
m = {}
for a, b in pairs:
    m.setdefault(b, set()).add(a)
print("\n--- iscl -> icla map (function test)")
bad = {k: v for k, v in m.items() if len(v) > 1}
print("   iscl values mapping to >1 icla:", bad)
print("   n distinct iscl:", len(m))
grp = {}
for a, b in pairs:
    grp.setdefault(a, set()).add(b)
for a in sorted(grp):
    print(f"   icla={a:2d} -> iscl {sorted(grp[a])}")
