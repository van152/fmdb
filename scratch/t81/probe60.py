"""t81-fix1 probe60 — schema field_codes + enums for inju/stgn/dscr; extension profile."""
import json
import runpy
import struct
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
core = runpy.run_path(str(REPO / "scripts" / "t73_mapper_core.py"), run_name="p60")
S = json.loads((REPO / "evidence/fm24/reports/editor_schema/master.json").read_text("utf-8"))

print("--- field_codes rows located in the three entities")
for code, rec in S["field_codes"].items():
    locs = rec.get("locations") or []
    for e in ("injury.xml#inju", "stage name.xml#stgn", "description.xml#dscr"):
        if any(e in l for l in locs):
            print(f"  {code:5s} {e:24s} {rec['name'][:32]:34s} {rec['type']}")
            break

print("--- enum value sets")
for name in ("icla", "iscl", "inSr", "Iagr", "Icms", "Icau"):
    v = S["enums"][name]["values"]
    ints = sorted(int(x["enum"]) for x in v if str(x["enum"]).lstrip("-").isdigit())
    print(f"  {name}: n={len(v)} ints={ints}")
