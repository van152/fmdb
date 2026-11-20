#!/usr/bin/env python3
"""Independent checks for t16b G1 inheritance and sampled naming bridges."""
from __future__ import annotations
import argparse, json, sys
from pathlib import Path

HERE = Path(__file__).resolve()
ROOT = HERE.parents[1] if HERE.parent.name == "scripts" else HERE.parents[3]
OUT = ROOT / "scratch/t16b/out"

def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))

def selftest() -> bool:
    assert compare((1, 2), [(1, 2)]) == "match"
    assert compare((1, 2), [(1, 4)]) == "conflict"
    assert compare((1, 2), []) == "missing"
    assert split_codes(["a", "b"], 8, 3) == [("a", 3, 4), ("b", 7, 4)]
    print("t16b verify selftest: PASS")
    return True

def compare(expected, observed):
    if expected in observed: return "match"
    return "conflict" if observed else "missing"

def split_codes(codes, width, offset):
    try: width, offset = int(width), int(offset)
    except (TypeError, ValueError): return []
    if width == 8 and len(codes) == 2:
        return [(codes[0], offset, 4), (codes[1], offset + 4, 4)]
    return [(x, offset, width) for x in codes]

def read_fields(tag: str) -> list[dict]:
    path = OUT / f"fields_{tag}.json"
    doc = load(path)
    if doc.get("storage") != "sharded":
        return doc.get("fields", [])
    rows = []
    for shard in doc.get("shards", []): rows.extend(load(OUT / shard).get("fields", []))
    return rows

def baselines(schema, stage2):
    refs = []
    weather = load(ROOT / "scratch/t01/inbox/t01l/output.json")["row_offset_map"]
    for code, item in weather.items():
        if code == "wnam": refs.append({"tag":"weat","field":code,"offset":None,"width":None,"table_type":27,"source":"scratch/t01/inbox/t01l/output.json"})
        else: refs.append({"tag":"weat","field":code,"offset":int(item.get("season",0))*23+int(item.get("nested_member_offset_in_season",0)),"width":int(item["width"]),"table_type":27,"source":"scratch/t01/inbox/t01l/output.json"})
    comp = load(ROOT / "scratch/t01/inbox/t01f/output.json")["row_offset_map"]
    for code, item in comp.items():
        if item.get("counted_as_new_schema_business_field"):
            refs.append({"tag":"comp","field":code,"offset":int(item["row_offset"]),"width":int(item["width"]),"table_type":25,"source":"scratch/t01/inbox/t01f/output.json"})
    entities = schema.get("entities", {})
    by_name = {name.lower(): obj.get("code") for name,obj in entities.items()}
    resolved = {x.get("entity") for x in stage2.get("tables",[]) if x.get("status")=="resolved"}
    accepted = {"readpair","ref_only","chain_unique","schema_fixed","ref_pair","full_shape_unique"}
    for slot in load(ROOT / "reports/t12_field_names.json").get("slots",[]):
        if slot.get("confidence") not in accepted: continue
        tag = by_name.get(str(slot.get("schema_entity","")).lower())
        if tag not in resolved: continue
        for code,off,wid in split_codes(slot.get("codes",[]),slot.get("width"),slot.get("row_off")):
            refs.append({"tag":tag,"field":code,"offset":off,"width":wid,"table_type":int(slot["type_id"]),"source":"reports/t12_field_names.json"})
    return refs

def verify() -> int:
    ledger = load(OUT / "ledger.json")
    schema = load(ROOT / "scratch/t05/schema_inventory.json")
    stage2 = load(ROOT / "scratch/t14/out/stage2_map.json")
    tags = sorted({x["entity"] for x in stage2.get("tables",[]) if x.get("status")=="resolved"})
    rows_by_tag = {tag: read_fields(tag) for tag in tags if (OUT / f"fields_{tag}.json").exists()}
    observations = {}
    sample = []
    codes = load(ROOT / "scratch/t12/out/codes_full.json")["codes"]
    sys.path.insert(0, str(ROOT / "scripts"))
    import t05_pe
    from capstone import CS_ARCH_X86, CS_MODE_64, Cs
    pe = t05_pe.PE(Path(r"<OLD_REPO>\input\editor.exe"))
    disasm = Cs(CS_ARCH_X86, CS_MODE_64)
    for tag, rows in rows_by_tag.items():
        for row in rows:
            ev = row.get("evidence", {})
            matches = ev.get("matches", [])
            if not matches: matches = ev.get("walk_candidates", [])
            for m in matches:
                key = (tag, row.get("field"), int(m["table_type"]))
                observations.setdefault(key, set()).add((int(m["offset"]),int(m["width"])))
            if row.get("grade") == "L3_instruction" and matches and len(sample) < 25:
                m = matches[0]
                instance = next((x for x in codes.get(m.get("4CC"), []) if x.get("file_off")==m.get("code_instance_offset")
                                 and x.get("shape")=="read" and x.get("object_off")==m.get("object_off")
                                 and x.get("size")==m.get("width")), None)
                byte_ok = False
                decoded = None
                if instance is not None:
                    va = int(instance["access_va"], 16)
                    file_off = pe.va2f(va)
                    ins = next(iter(disasm.disasm(pe.raw[file_off:file_off+16], va, count=1)), None) if file_off is not None else None
                    if ins is not None:
                        decoded = f"{ins.mnemonic} {ins.op_str}"
                        byte_ok = (decoded == instance.get("instruction") and
                                   hex(ins.address) == instance.get("access_va"))
                ok = instance is not None and m.get("4CC") == row.get("field")
                sample.append({"tag":tag,"field":row.get("field"),"bridge_instance_ok":ok,
                               "instruction_recalc_ok":byte_ok,"recalculated_instruction":decoded,
                               "offset":m.get("offset"),"width":m.get("width"),"table_type":m.get("table_type")})
    checks=[]
    for ref in baselines(schema,stage2):
        if ref["tag"] not in rows_by_tag: continue
        if ref["offset"] is None or ref["width"] is None:
            checks.append({**ref,"status":"not_comparable"}); continue
        obs=sorted(observations.get((ref["tag"],ref["field"],ref["table_type"]),set()))
        checks.append({**ref,"observed":[list(x) for x in obs],"status":compare((ref["offset"],ref["width"]),obs)})
    comparable=[x for x in checks if x["status"]!="not_comparable"]
    matches=sum(x["status"]=="match" for x in comparable)
    rate=matches/len(comparable) if comparable else None
    recorded=ledger.get("g1",{})
    errors=[]
    if matches != recorded.get("matches") or len(comparable) != recorded.get("compared"):
        errors.append("G1 aggregate does not reproduce")
    if rate != recorded.get("consistency"):
        errors.append("G1 consistency does not reproduce")
    if recorded.get("status") != ("pass" if rate is not None and rate >= .95 else "fail"):
        errors.append("G1 threshold status inconsistent")
    bad_samples=[x for x in sample if not x["bridge_instance_ok"] or not x["instruction_recalc_ok"]]
    if bad_samples: errors.append("sampled bridge or editor.exe instruction recalculation failed")
    g1_pass = rate is not None and rate >= .95
    result={"status":"pass" if not errors and g1_pass else "fail",
            "verification_recalculation":"pass" if not errors else "fail",
            "g1_matches":matches,"g1_compared":len(comparable),"g1_consistency":rate,
            "g1_threshold":.95,"g1_recorded_status":recorded.get("status"),"sampled_bridges":sample,
            "errors":errors,"acceptance_failures":[] if g1_pass else ["G1 consistency below 95%"]}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if not errors and g1_pass else 1

def main(argv=None):
    global OUT
    ap=argparse.ArgumentParser(description="Verify t16b inherited offsets and sample exact naming bridges.")
    ap.add_argument("--outdir",default=str(OUT),help="ledger directory (default scratch/t16b/out)")
    ap.add_argument("--selftest",action="store_true",help="test comparison and split helpers")
    args=ap.parse_args(argv)
    if args.selftest: return 0 if selftest() else 1
    OUT=Path(args.outdir)
    try: return verify()
    except Exception as exc:
        print(f"fatal: {type(exc).__name__}: {exc}",file=sys.stderr)
        return 2

if __name__=="__main__": raise SystemExit(main())
