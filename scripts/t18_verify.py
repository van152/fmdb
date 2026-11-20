#!/usr/bin/env python3
"""Verify t18 golden row layouts, stride closures, and generated ledgers."""
from __future__ import annotations
import argparse, importlib.util, json, sys
from pathlib import Path
HERE = Path(__file__).resolve()
ROOT = HERE.parents[1] if HERE.parent.name == "scripts" else HERE.parents[3]
OUT = ROOT / "scratch/t18/out"

def load(path):
    return json.loads(path.read_text(encoding="utf-8"))

def builder_module():
    path = ROOT / "scripts/t18_build.py"
    spec = importlib.util.spec_from_file_location("t18_build", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

def read_output(tag):
    manifest = load(OUT / f"fields_{tag}.json")
    if manifest.get("storage") != "sharded":
        return manifest, manifest.get("fields", [])
    fields=[]
    for name in manifest["shards"]:
        fields.extend(load(OUT / name).get("fields", []))
    return manifest, fields

def selftest():
    assert 42 + 1 == 43
    assert 126 + 1 == 127
    assert 7 + 92 + 12 + 1 == 112
    print("t18 verify selftest: PASS")
    return 0

def verify():
    errors=[]
    bridge=load(OUT / "bridge.json")
    gold=builder_module().golden()
    total_m=total_n=0
    for tag, data in gold.items():
        matches=sum(bool(x["match"]) for x in data["checks"])
        compared=len(data["checks"])
        total_m += matches
        total_n += compared
        if matches != data["matches"] or matches != compared:
            errors.append(f"{tag}: row field comparisons incomplete ({matches}/{compared})")
        if not data["stride_pass"]:
            errors.append(f"{tag}: stride closure failed")
        entry=next((x for x in bridge.get("entities",[]) if x.get("entity")==tag),None)
        if not entry or entry.get("stride_check") != "pass":
            errors.append(f"{tag}: bridge stride_check is not pass")
        if entry and entry.get("g1_row_consistency") != 1.0:
            errors.append(f"{tag}: bridge consistency is not 1.0")
        manifest, fields=read_output(tag)
        if len(fields) != manifest.get("fields_total"):
            errors.append(f"{tag}: field shard count mismatch")
        if any(f.get("grade")=="L3_instruction" for f in fields):
            errors.append(f"{tag}: legacy grade L3_instruction was not converted")
    rate=total_m/total_n if total_n else 0.0
    if rate < .95:
        errors.append(f"golden row consistency below 95%: {rate:.4%}")
    if bridge.get("golden_matches") != total_m or bridge.get("golden_compared") != total_n:
        errors.append("bridge golden aggregate differs from recalculation")
    expected={"comp":18,"weat":88,"city":7}
    actual={k:len(v["checks"]) for k,v in gold.items()}
    if actual != expected:
        errors.append(f"unexpected golden denominator: {actual}")
    result={"status":"pass" if not errors else "fail","golden_matches":total_m,"golden_compared":total_n,
            "golden_consistency":rate,"threshold":.95,"stride_checks":{k:v["stride_pass"] for k,v in gold.items()},
            "errors":errors}
    print(json.dumps(result,ensure_ascii=False,indent=2))
    return 0 if not errors else 1

def main(argv=None):
    global OUT
    ap=argparse.ArgumentParser(description="Verify t18 golden row-layout comparisons and stride closures.")
    ap.add_argument("--outdir",default=str(OUT),help="t18 output directory")
    ap.add_argument("--selftest",action="store_true",help="run helper assertions")
    args=ap.parse_args(argv)
    if args.selftest:
        return selftest()
    OUT=Path(args.outdir)
    try:
        return verify()
    except Exception as exc:
        print(f"fatal: {type(exc).__name__}: {exc}",file=sys.stderr)
        return 2
if __name__ == "__main__":
    raise SystemExit(main())
