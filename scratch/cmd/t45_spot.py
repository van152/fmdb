#!/usr/bin/env python3
"""Commander independent spot for t45 schema v3 (52 L3, Csme merge, v2 preservation)."""
import json, pathlib, sys
ROOT = pathlib.Path(r"D:/tmp2b/fm24-db")
d = json.load(open(ROOT / "reports/club_nation_subtable_schema.json", encoding="utf-8"))
P = F = 0
def ck(n, c, x=""):
    global P, F
    if c: P += 1; print(f"PASS {n} {x}")
    else: F += 1; print(f"FAIL {n} {x}")
ck("version 3", d.get("schema_version") == 3)
tables = d["tables"]
ck("8 tables", len(tables) == 8)
want = {"Cstc":14,"Clhs":8,"CSrs":10,"Cmti":5,"CNtp":2,"Cdbt":5,"Tchl":7,"Csme":1}
for t in tables:
    ck(f"{t['parent_code']} count", len(t["fields"]) == want[t["parent_code"]], f"{len(t['fields'])}")
l3 = [f for t in tables for f in t["fields"] if f.get("status") == "L3"]
ck("total L3 == 52", len(l3) == 52, str(len(l3)))
ck("coverage 52/16/4/0", (d["coverage"]["club_L3_fields"],d["coverage"]["held_fields"],d["coverage"]["negative_regressions"],d["coverage"]["L4"]) == (52,16,4,0))
ck("held actual == 16", sum(len(t.get("held_fields",[])) for t in tables) == 16)
ck("master SHA cited", "7d57477e" in json.dumps(d, ensure_ascii=False))
csme = next(t for t in tables if t["parent_code"] == "Csme")
ck("Csme tt59 src t41", csme["table_type"] == 59 and csme.get("source_task") == "t41")
ck("Csme Melf L3", [f["code"] for f in csme["fields"]] == ["Melf"] and csme["fields"][0]["status"] == "L3")
ck("Csme Msid held", [f.get("code") for f in csme.get("held_fields",[])] == ["Msid"])
# Csme variable closure
sp = csme.get("server_payload", {})
cl = csme.get("closure") or sp.get("closure") or {}
eq = json.dumps(cl, ensure_ascii=False) + json.dumps(sp, ensure_ascii=False)
ck("Csme closure 224880 mentioned", "224880" in eq, eq[:80])
# v2 preservation
v2p = ROOT / "scratch/t45/out/club_nation_subtable_schema.v2.json"
ck("v2 snapshot exists", v2p.exists())
if v2p.exists():
    v2 = json.load(open(v2p, encoding="utf-8"))
    v2t = {t["parent_code"]: t for t in v2["tables"]}
    ck("v2 has 7 tables 51 L3", len(v2["tables"]) == 7 and sum(len(t["fields"]) for t in v2["tables"]) == 51)
    unchanged = all(json.dumps(t["fields"], sort_keys=True) == json.dumps(v2t[t["parent_code"]]["fields"], sort_keys=True) for t in tables if t["parent_code"] in v2t)
    ck("v2 seven tables fields verbatim in v3", unchanged)
print(f"--- {P} PASS / {F} FAIL ---")
sys.exit(0 if F == 0 else 1)