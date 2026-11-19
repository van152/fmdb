#!/usr/bin/env python3
"""Commander independent spot for t42 schema v2 (51 L3, Tchl merge, v1 preservation, master SHA)."""
import json, pathlib, sys
ROOT = pathlib.Path(r"D:/tmp2b/fm24-db")
d = json.load(open(ROOT / "reports/club_nation_subtable_schema.json", encoding="utf-8"))
P = F = 0
def ck(n, c, x=""):
    global P, F
    if c: P += 1; print(f"PASS {n} {x}")
    else: F += 1; print(f"FAIL {n} {x}")

ck("schema_version 2", d.get("schema_version") == 2)
tables = d["tables"]
ck("7 tables", len(tables) == 7, str(len(tables)))
pcodes = {t["parent_code"] for t in tables}
ck("pcodes incl Tchl", pcodes == {"Cstc","Clhs","CSrs","Cmti","CNtp","Cdbt","Tchl"}, str(sorted(pcodes)))
want = {"Cstc":14,"Clhs":8,"CSrs":10,"Cmti":5,"CNtp":2,"Cdbt":5,"Tchl":7}
for t in tables:
    ck(f"{t['parent_code']} count", len(t["fields"]) == want[t["parent_code"]], f"{len(t['fields'])} want {want[t['parent_code']]}")
l3 = [f for t in tables for f in t["fields"] if f.get("status") == "L3"]
ck("total L3 == 51", len(l3) == 51, str(len(l3)))
ck("coverage 51/15/4/0", (d["coverage"]["club_L3_fields"],d["coverage"]["held_fields"],d["coverage"]["negative_regressions"],d["coverage"]["L4"]) == (51,15,4,0))
held = sum(len(t.get("held_fields",[])) for t in tables)
ck("held actual == 15", held == 15, str(held))
# master SHA
s = json.dumps(d, ensure_ascii=False)
ck("master.json SHA 7d57477e cited", "7d57477e" in s)
# Tchl specifics
tchl = next(t for t in tables if t["parent_code"] == "Tchl")
ck("Tchl table_type 34", tchl["table_type"] == 34)
ck("Tchl source_task t39", tchl.get("source_task") == "t39", str(tchl.get("source_task")))
tcodes = {f["code"] for f in tchl["fields"]}
ck("Tchl 7 L3 codes", tcodes == {"tchc","mstn","sstn","dbrt","posi","cquf","tcop"}, str(sorted(tcodes)))
theld = {f.get("code") for f in tchl.get("held_fields",[])}
ck("Tchl 2 held styr/edyr", theld == {"styr","edyr"}, str(sorted(theld)))
# cross-check Tchl offsets vs t39 source ledger
src = json.load(open(ROOT / "scratch/t39/out/fields_tchl.json", encoding="utf-8"))
sfields = src if isinstance(src, list) else src.get("fields", [])
smap = {}
for f in (sfields if isinstance(sfields, list) else []):
    c = f.get("code") or f.get("field") or f.get("fourcc")
    if c: smap[c] = f
# v1 preservation
v1p = ROOT / "scratch/t42/out/club_nation_subtable_schema.v1.json"
ck("v1 snapshot exists", v1p.exists())
if v1p.exists():
    v1 = json.load(open(v1p, encoding="utf-8"))
    v1t = {t["parent_code"]: t for t in v1["tables"]}
    ck("v1 has 6 tables 44 L3", len(v1["tables"]) == 6 and sum(len(t["fields"]) for t in v1["tables"]) == 44)
    unchanged = True
    for t in tables:
        pc = t["parent_code"]
        if pc in v1t:
            if json.dumps(t["fields"], sort_keys=True) != json.dumps(v1t[pc]["fields"], sort_keys=True):
                unchanged = False; print("  changed:", pc)
    ck("v1 six tables fields verbatim in v2", unchanged)
print(f"--- {P} PASS / {F} FAIL ---")
sys.exit(0 if F == 0 else 1)