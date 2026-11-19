#!/usr/bin/env python3
"""Commander independent spot for t40 consolidated schema (structure/provenance/count consistency)."""
import json, pathlib, sys
ROOT = pathlib.Path(r"D:/tmp2b/fm24-db")
d = json.load(open(ROOT / "reports/club_nation_subtable_schema.json", encoding="utf-8"))
P = F = 0
def ck(n, c, x=""):
    global P, F
    if c: P += 1; print(f"PASS {n} {x}")
    else: F += 1; print(f"FAIL {n} {x}")

tables = d["tables"]
ck("6 tables", len(tables) == 6, str(len(tables)))
pcodes = {t["parent_code"] for t in tables}
ck("parent_codes", pcodes == {"Cstc","Clhs","CSrs","Cmti","CNtp","Cdbt"}, str(sorted(pcodes)))
ttypes = {t["table_type"] for t in tables}
ck("table_types", ttypes == {22,37,62,43,66,33}, str(sorted(ttypes)))
# per-table field counts
want_counts = {"Cstc":14,"Clhs":8,"CSrs":10,"Cmti":5,"CNtp":2,"Cdbt":5}
for t in tables:
    n = len(t["fields"])
    ck(f"{t['parent_code']} field count", n == want_counts[t["parent_code"]], f"{n} want {want_counts[t['parent_code']]}")
# L3 count
l3 = [f for t in tables for f in t["fields"] if f.get("status") == "L3"]
ck("total L3 fields == 44", len(l3) == 44, str(len(l3)))
ck("coverage.club_L3_fields == actual", d["coverage"]["club_L3_fields"] == len(l3), str(d["coverage"]["club_L3_fields"]))
ck("coverage.L4 == 0", d["coverage"]["L4"] == 0)
# field completeness
missing = []
for f in l3:
    for k in ("code","row_offset","wire_offset","width_bytes","interpretation","schema"):
        if k not in f: missing.append((f.get("code"), k))
ck("all L3 fields complete", not missing, str(missing[:5]))
# held count consistency
held = sum(len(t.get("held_fields", [])) for t in tables)
ck("held count == coverage", held == d["coverage"]["held_fields"], f"{held} vs {d['coverage']['held_fields']}")
ck("negative_regressions == 4", len(d["negative_regressions"]) == 4 == d["coverage"]["negative_regressions"])
# provenance
for t in tables:
    ck(f"{t['parent_code']} source_task", bool(t.get("source_task")), str(t.get("source_task")))
bp = d.get("binary_provenance", {})
bpstr = json.dumps(bp)
ck("editor.exe SHA b82ebe8e in provenance", "b82ebe8e" in bpstr)
ck("master.json SHA 7d57477e in provenance", "7d57477e" in bpstr or "7d57477e" in json.dumps(d.get("source_artifacts")))
# closure arithmetic for fixed-stride tables (server_payload)
for t in tables:
    sp = t.get("server_payload", {})
    cl = t.get("closure") or sp.get("closure") or {}
    eq = cl.get("equation") if isinstance(cl, dict) else None
    n = sp.get("count"); st = sp.get("stride"); pl = sp.get("payload_size") or sp.get("payload_len")
    if n and st and pl:
        ok = (14 + n*st + 8 == pl) or (13 + n*st + 9 == pl)
        ck(f"{t['parent_code']} closure arithmetic", ok, f"14+{n}*{st}+8={14+n*st+8} vs {pl}")
print(f"--- {P} PASS / {F} FAIL ---")
sys.exit(0 if F == 0 else 1)