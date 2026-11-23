#!/usr/bin/env python3
"""Independent integrity check for t116 output; read-only."""
import hashlib,json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[3]
OUT=ROOT/"scratch/t116/out"
def sha(p):
 h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()
def main():
 d=json.loads((OUT/"wave13_consolidated.json").read_text(encoding="utf-8")); errors=[]
 if d.get("status")!="complete": errors.append("status")
 for a in d.get("artifacts",[]):
  if not a.get("present",True): continue
  p=ROOT/a["path"]
  if not p.exists(): errors.append("missing:"+a["path"]); continue
  if a.get("sha256") and sha(p)!=a["sha256"]: errors.append("sha256:"+a["path"])
 c=json.loads((OUT/"ledger_candidates.json").read_text(encoding="utf-8"))
 ids=[e.get("id") for e in c.get("entries",[])]
 if ids!=["E%d"%i for i in range(142,151)]: errors.append("candidate_ids")
 if c.get("status")!="draft_not_ledgered": errors.append("candidate_status")
 if errors: print("FAIL",*errors,sep="\n"); return 1
 print("PASS artifacts=%d candidates=%d regressions=%d"%(len(d.get("artifacts",[])),len(ids),len(d.get("regression_matrix",[])))); return 0
if __name__=="__main__": sys.exit(main())
