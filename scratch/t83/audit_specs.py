import json, os, struct, sys
from pathlib import Path
from collections import Counter

ROOT = Path(r"D:\tmp2b\fm24-db")
sys.path.append(r"D:\tmp2b\fm24\tools\python")
import numpy as np
import zstandard as zstd

DB_DIR = Path(os.environ.get("FM24_DB_DIR", str(ROOT / "scratch/data")))
master = json.loads((ROOT / "evidence/fm24/reports/editor_schema/master.json").read_text(encoding="utf-8"))
enums = master["enums"]

# Dump ALL 188 XML fields cleanly with exact constraints (min/max/enum_values/enum_ref/type/optional)
out = []
ent_keys = ["award.xml", "language.xml", "weather.xml", "derby.xml", "media source.xml"]
xml_specs = {}
for ek in ent_keys:
    rec = master["entities"][ek][0]
    fields = rec["fields"]
    xml_specs[ek] = fields
    out.append(f"\n================ {ek} ({len(fields)} fields) ================")
    for idx, f in enumerate(fields):
        fid = f["field"]
        nm = f.get("name")
        tp = f.get("type")
        mn = f.get("min_value", f.get("min"))
        mx = f.get("max_value", f.get("max"))
        ev = f.get("enum_values")
        eref = f.get("enum_id") or f.get("enum") or f.get("list_id") or f.get("enum_ref")
        # check all keys on field
        rest = {k: v for k, v in f.items() if k not in ("field", "name", "type", "raw_name", "dependencies", "enum_values")}
        ev_str = ""
        if ev:
            ev_ids = [x.get("enum_id", x.get("enum")) for x in ev]
            ev_str = f" enum_values({len(ev_ids)})={ev_ids[:15]}" + ("..." if len(ev_ids) > 15 else "")
        out.append(f"  [{idx:2d}] {fid:5s} | {tp:26s} | {nm:36s} | rest={json.dumps(rest, ensure_ascii=False)[:140]}{ev_str}")

# Also inspect unique occurrence count of each of our 188 field codes across ALL master.json entities (Gate 1!)
code_occ = Counter()
for ek, recs in master["entities"].items():
    for rec in recs:
        for f in rec.get("fields", []):
            code_occ[f["field"]] += 1

out.append("\n================ GATE 1 OCCURRENCE COUNTS (>1) ================")
for ek in ent_keys:
    dups = [(f["field"], code_occ[f["field"]]) for f in xml_specs[ek] if code_occ[f["field"]] > 1]
    out.append(f"  {ek}: multi-entity fields = {dups}")

# Also check if t76c slots have anything else we must reconcile
for p in sorted((ROOT / "scratch/t76c/out").glob("slots_*.json")):
    d = json.loads(p.read_text(encoding="utf-8"))
    out.append(f"\n--- t76c {p.name} keys={list(d.keys())} ---")
    slots = d.get("slots", [])
    for s in slots[:40]:
        out.append(f"  {json.dumps(s, ensure_ascii=False)[:180]}")

Path(r"D:\tmp2b\fm24-db\scratch\t83\audit_specs_and_t76c.txt").write_text("\n".join(out), encoding="utf-8")
print("Wrote audit_specs_and_t76c.txt, lines:", len(out))
