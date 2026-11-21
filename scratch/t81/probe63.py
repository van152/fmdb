"""t81-fix1 probe63 — exhaustive master-enum search for t6 bytes; labeled row dump."""
import json
import runpy
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p63")
M = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text("utf-8"))

ENUMS = {}
for name, rec in M["enums"].items():
    ints = {int(v["enum"]) for v in rec.get("values", [])
            if str(v["enum"]).lstrip("-").isdigit()}
    if ints:
        ENUMS[name] = ints

raw_c = core["load_payload"]("client", 6)
n = 115
col0 = {raw_c[14 + j * 16] for j in range(n)}
col1 = {raw_c[14 + j * 16 + 1] for j in range(n)}

print("--- enums whose int set == col0 exactly:", [k for k, v in ENUMS.items() if v == col0])
print("--- enums that contain col0:", [k for k, v in ENUMS.items() if col0 <= v])
print("--- enums whose int set == col1 exactly:", [k for k, v in ENUMS.items() if v == col1])
print("--- enums that contain col1:", [k for k, v in ENUMS.items() if col1 <= v])
print("--- col0:", sorted(col0))
print("--- icla:", sorted(ENUMS["icla"]), "| in icla not data:", sorted(ENUMS['icla'] - col0),
      "| in data not icla:", sorted(col0 - ENUMS['icla']))
print("--- iscl missing:", sorted(ENUMS['iscl'] - col1), "| extra:", sorted(col1 - ENUMS['iscl']))

# labeled dump: server row 0 and 114 with 27-byte business layout
raw_s = core["load_payload"]("server", 6)
for j in (0, 1, 114):
    r = raw_s[14 + j * 40: 14 + j * 40 + 40]
    print(f"server row{j} biz:", " ".join(f"{i:02d}:{b:02x}" for i, b in enumerate(r[:27])))
    print(f"   ident:", r[27:40].hex())
