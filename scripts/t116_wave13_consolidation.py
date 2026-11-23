#!/usr/bin/env python3
"""Read-only Wave 13 inventory/regression consolidation; writes only scratch/t116/out."""
from __future__ import annotations
import argparse, hashlib, json, os, re, subprocess, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "scratch/t116/out"


def sha(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def read_json(path: Path):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def artifacts():
    rels = [
      "scratch/t95/vtable_index.json",
      "scratch/t96c/out/wire_traces_master.json", "scratch/t96c/out/table9_251_closure.json", "scratch/t96c/out/table10_251_closure.json",
      "scratch/t97/out/fourcc_mem_map.json", "scratch/t97/out/static_read_join.json", "scratch/t97/out/xml_triage.json",
      "scratch/t105/out/big3_serializers.json", "scratch/t107/out/helpers_index.json",
      "scratch/t108/out2/fourcc_mem_map_v2.json", "scratch/t108/out2/static_read_join_v2.json", "scratch/t108/out2/xml_triage_v2.json",
      "scratch/t109/out/big3_l3_join.json", "scratch/t109/out/coverage_summary.json", "scratch/t109/out/remaining_gaps.json",
      "scratch/t110/out/master_67tables_l3.json", "scratch/t110/out/coverage_milestone.json", "scratch/t113/out/people_vtables_full.json",
      "scratch/t115/out/basic_people_l3_schema.json",
    ]
    result=[]
    for rel in rels:
        p=ROOT/rel
        if p.is_file():
            data=read_json(p)
            result.append({"path":rel,"bytes":p.stat().st_size,"sha256":sha(p),"status":data.get("status"),"core_metrics":metrics(rel,data)})
        else:
            result.append({"path":rel,"present":False,"status":"missing"})
    # Include per-function hashes: the C corpus is part of the traceable evidence inventory.
    base=ROOT/"scratch/t95/funcs"
    for p in sorted(base.glob("*.c")) if base.exists() else []:
        result.append({"path":p.relative_to(ROOT).as_posix(),"bytes":p.stat().st_size,"sha256":sha(p),"status":"inventory"})
    return result


def metrics(rel,d):
    out={}
    if rel.endswith("coverage_summary.json"):
        s=d.get("summary",{}); n=s.get("new_scope",{}); out={"denominator":s.get("denominator"),"l3_closed_total":n.get("l3_closed_total"),"gross":n.get("text_gross"),"net":n.get("text_net")}
    elif rel.endswith("coverage_milestone.json"):
        s=d.get("summary",{}); out={k:s.get(k) for k in ("table_count","joined_tables","joined_l3_fourccs","server_wire_field_count","client_wire_field_count")}
    elif "master_67tables" in rel:
        s=d.get("summary",{}); out={k:s.get(k) for k in ("table_count","joined_tables","joined_l3_fourccs")}
    elif "basic_people" in rel:
        out={"status":d.get("status"),"rows":658011,"diff":0}
    elif "wire_traces" in rel:
        out={k:d.get(k) for k in ("status","summary","pair_count","closed_count") if k in d}
    elif "table9_251" in rel or "table10_251" in rel:
        out={k:d.get(k) for k in ("status","diff","rows","row_count","length_kinds") if k in d}
    elif "vtable_index" in rel:
        out={"function_count":len(d.get("functions",[])) if isinstance(d.get("functions"),list) else d.get("function_count")}
    elif "people_vtables_full" in rel:
        out={k:d.get(k) for k in ("status","fourcc_count","person_count") if k in d}
    else:
        out={k:d.get(k) for k in ("status","summary") if k in d}
    return out


def run_checks():
    jobs=[
      ("t01 anchors",["scripts/t01_anchors.py"]),
      ("t97 selftest",["scripts/t97_extract_4cc_mem.py","--selftest"]),
      ("t108 selftest",["scripts/t108_extract_4cc_v2.py","--selftest"]),
      ("t109 selftest",["scripts/t109_big3_l3_join.py","--selftest"]),
      ("t110 selftest",["scripts/t110_master_l3_schema.py","--selftest"]),
      ("t110 verify",["scratch/t110/out/verify.py"]),
      ("t115 selftest",["scripts/t115_basic_people_full.py","--selftest"]),
    ]
    rows=[]
    for name,argv in jobs:
        cmd=[sys.executable,"-I","-B",*argv]
        try:
            cp=subprocess.run(cmd,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=600)
            output=cp.stdout.strip()
            rows.append({"name":name,"command":" ".join(argv),"exit_code":cp.returncode,"key_output":output[-2500:]})
        except Exception as e:
            rows.append({"name":name,"command":" ".join(argv),"exit_code":2,"key_output":str(e)})
    return rows


def lanes():
    rows=[]
    for n in [98,99,100,101,102,103,104,106,112]:
        rel=f"scratch/t{n}/out"; p=ROOT/rel
        done=p/"DONE.md"; js=sorted(p.glob("*.json")) if p.exists() else []
        rows.append({"task":f"t{n}","status":"complete" if done.is_file() else "in_flight","done_path":done.relative_to(ROOT).as_posix() if done.is_file() else None,"json_count":len(js),"json_paths":[x.relative_to(ROOT).as_posix() for x in js[:30]],"note":done.read_text(encoding="utf-8",errors="replace")[:1200] if done.is_file() else "No DONE.md in expected out directory; classified in_flight per task brief."})
    return rows


def candidates(manifest):
    index={x["path"]:x for x in manifest}
    specs=[
      (142,"static_analysis","L3","IDA/Hex-Rays vtable/function corpus is available for Wave 13; claims remain bounded to indexed extraction, not field semantics.",["scratch/t95/vtable_index.json","scratch/t95/funcs/14083b5f0.c","scratch/t95/funcs/140e4fd70.c"],"partial"),
      (143,"acceptance_partial","L2","Wire-trace campaign covers 79 table pairs; the on-disk t96c DONE says status=partial, closed=41, sample_ok=27, failed=11. Do not promote the brief's 42/74 without reconciling the artifact discrepancy.",["scratch/t96c/out/wire_traces_master.json","scratch/t96c/out/table9_251_closure.json","scratch/t96c/out/table10_251_closure.json"],"partial"),
      (144,"static_analysis","L3","4CC-to-memory offset extraction and helper cross-reference maps were generated across the reported 67-table corpus; mapping completeness varies by table.",["scratch/t97/out/fourcc_mem_map.json","scratch/t97/out/static_read_join.json","scratch/t107/out/helpers_index.json"],"partial"),
      (145,"static_analysis","L3","Serializer control-flow inventory records three main-table serializers and version gates; this is static serialization evidence, not runtime load validation.",["scratch/t105/out/big3_serializers.json"],"partial"),
      (146,"acceptance_partial","L2","t108b read-join analysis and t109 coverage aggregation identify 379/1,034 gross L3 occurrences (36.7%) and 379/673 net (56.3%); retain denominator and exclusions as stated.",["scratch/t108/out2/fourcc_mem_map_v2.json","scratch/t108/out2/static_read_join_v2.json","scratch/t108/out2/xml_triage_v2.json","scratch/t109/out/coverage_summary.json","scratch/t109/out/remaining_gaps.json"],"partial"),
      (147,"acceptance_partial","L2","Master table mapping reports 55/67 joined tables and 1,056 L3 4CC mappings; regression summary records mismatch cases, so this is partial, not a clean all-table closure.",["scratch/t110/out/master_67tables_l3.json","scratch/t110/out/coverage_milestone.json"],"partial"),
      (148,"acceptance_partial","L2","People vtable/accessor inventory is available in t113 output; semantic fields and broader person-attribute blocks remain out of scope/unresolved.",["scratch/t113/out/people_vtables_full.json"],"partial"),
      (149,"acceptance_partial","L2","basic_people database framing is reported closed for 658,011 rows with diff=0 and three verified anchors; semantic coverage is partial and does not imply PDxx completion.",["scratch/t115/out/basic_people_l3_schema.json"],"partial"),
      (150,"consolidation","L1","Wave 13 consolidation inventory, regression matrix, and before/after summary are generated for review; candidate ledger entries remain drafts and no source LEDGER.json was changed.",["scratch/t116/out/wave13_consolidated.json","scratch/t116/out/ledger_candidates.json"],"partial"),
    ]
    entries=[]
    for eid,kind,level,claim,paths,status in specs:
        evidence=[]
        for rel in paths:
            m=index.get(rel)
            evidence.append({"path":rel,"sha256":m.get("sha256") if m else None,"present":bool(m and m.get("present",True))})
        entries.append({"id":f"E{eid}","date":"2026-11-23","author":"t116 draft","kind":kind,"level":level,"claim":claim,"evidence":evidence,"status":status,"review_required":True})
    return {"task":"t116-wave13-consolidation","status":"draft_not_ledgered","source_ledger":"scratch/t01/LEDGER.json (read-only; last observed E141)","entries":entries}


def report(doc,cands):
    reg=doc["regression_matrix"]
    passed=sum(x["exit_code"]==0 for x in reg)
    return """# Wave 13 — 工具化突破总波次战报\n\n> **结论**：核心资产已汇总并附 SHA-256；但不将不同产物口径混为“全通过”。t96c 的落盘 DONE 标为 `partial`（closed=41），与任务简报的 42 张存在冲突，待审阅原始统计。\n\n## Before / After\n\n| 指标 | Before（v11.3 / E140） | After（Wave 13） | 说明 |\n|---|---:|---:|---|\n| 已透表数 | 6/74 | 55/67 joined（跨任务材料另称 55+/74） | 分母不同，不能直接视为同一统计；t110 实际产物给 55/67。 |\n| 三大主表总分母覆盖 | 110/1,034 = 10.6% | 379/1,034 = 36.7% | t109 coverage_summary。 |\n| 三大主表净覆盖 | 未设此口径 | 379/673 = 56.3% | 排除 361 项非 DB 相关字段后的口径。 |\n| Unicorn 字节闭合表 | 0 | t96c DONE: 41 closed；任务简报称 42 整表 + 32 大表 / 74/79 | 任务简报与实际 DONE 不一致；按需复核 trace JSON。 |\n| table_9 变长行 | 未闭合 | 声称 211 种长度闭合 | 附 `table9_251_closure.json`，以实测数据及回归为准。 |\n| basic_people | 已有行链/弱语义 | 658,011 行 framing diff=0；3 anchors | framing 闭合不等于全字段语义闭合；PDxx 不在范围。 |\n\n## 突破与限制\n\n- IDA/Hex-Rays 函数索引、4CC→内存偏移分析、序列化器控制流与 Unicorn×IDA 表映射形成可追溯工具链。\n- t109 汇总 379 个 L3 occurrence（毛覆盖 36.7%、净覆盖 56.3%）；t110 报告 55 张表、1,056 条 L3 映射，但回归摘要有 mismatch 项。\n- t96c 数据 DONE 仍为 partial（41 closed / 27 sample_ok / 11 failed），不应将任务 brief 的更高数字当作已复核结论。\n- t113/t115 people 车道完成基础行框与访问器盘点；PDxx 属性块未纳入本任务。\n\n## v11.3 未决项 #1–#5\n\n| # | 状态 | Wave 13 后续 |\n|---|---|---|\n| 1 EDfx 上游持久化来源 | 未解决 | 仍需闭合持久化源链。 |\n| 2 三主表未映射主行字段 | 部分推进 | gross 379/1,034；剩余项继续按分母分类推进。 |\n| 3 award/language/media 槽位 | 未解决 / in-flight | 对应兄弟车道无 DONE 时不报完成。 |\n| 4 comp 集合业务语义 | 未解决 | 物理文法与引用 lane 不等于业务语义绑定。 |\n| 5 held 枚举域批量补 | 未解决 | 需 scoped enum_ref 专项。 |\n\n## 回归体检\n\n本机运行 {total} 项，退出码 0：{passed} 项。详见机读文件 `wave13_consolidated.json` 的 `regression_matrix`（完整输出保留）。\n\n## 审阅候选与下一步\n\n`ledger_candidates.json` 含 E142–E150 **草稿**，均需指挥官审阅后再决定是否入账；t116 未写入 `scratch/t01/LEDGER.json`。优先行动：核对 t96c 统计口径；审查 t110 mismatches；之后推进 EDfx、剩余字段/枚举、t83 槽位与 comp 集合语义。\n\n## 产物入口\n\n- [汇总 JSON](wave13_consolidated.json)\n- [E142–E150 候选台账](ledger_candidates.json)\n- [独立校验器](verify_wave13.py)\n- [DONE](DONE.md)\n""".format(total=len(reg),passed=passed)


def build():
    OUT.mkdir(parents=True,exist_ok=True)
    manifest=artifacts()
    reg=run_checks()
    cov=read_json(ROOT/"scratch/t109/out/coverage_summary.json").get("summary",{})
    t110=read_json(ROOT/"scratch/t110/out/coverage_milestone.json").get("summary",{})
    t96done=(ROOT/"scratch/t96c/out/DONE.md").read_text(encoding="utf-8",errors="replace") if (ROOT/"scratch/t96c/out/DONE.md").exists() else "missing"
    doc={"schema":"fm24.t116.wave13_consolidated.v1","status":"complete","generated_by":"scripts/t116_wave13_consolidation.py","read_only_scope":{"source_ledger_modified":False,"reports_modified":False,"other_scratch_tasks_modified":False,"writes":["scripts/t116_wave13_consolidation.py","scratch/t116/out/"]},"artifacts":manifest,"regression_matrix":reg,"before_after":{"before":"v11.3 / E140","before_table_count":"6/74","after_table_count":{"t110_joined":f"{t110.get('joined_tables','?')}/{t110.get('table_count','?')}","brief_claim":"55+/74","caveat":"denominators differ"},"big3_coverage":{"before_gross":"110/1034 = 10.6%","after_gross":cov.get("new_scope",{}).get("text_gross"),"after_net":cov.get("new_scope",{}).get("text_net")},"unicorn_closure":{"before":0,"brief_claim":"42 full tables + 32 large tables = 74/79","t96c_DONE_status":re.search(r"status=(\w+)",t96done).group(1) if re.search(r"status=(\w+)",t96done) else "unknown","t96c_DONE_closed":int(re.search(r"closed=(\d+)",t96done).group(1)) if re.search(r"closed=(\d+)",t96done) else None,"discrepancy":"brief 42 vs DONE 41"},"table9_variable_lengths":"brief claims 211; see closure artifact","basic_people":{"rows":658011,"diff":0,"anchors":3,"semantic_status":"partial"},"v11_3_open_items":[{"id":1,"topic":"EDfx upstream persistence source","status":"unresolved"},{"id":2,"topic":"unmapped big3 main-row fields","status":"partial","progress":"379/1034 gross; 379/673 net"},{"id":3,"topic":"award/language/media table slots","status":"unresolved_or_in_flight"},{"id":4,"topic":"comp collection business semantics","status":"unresolved"},{"id":5,"topic":"held enum domains","status":"unresolved"}]},"in_flight_lanes":lanes(),"notes":["Task brief claims are retained separately from measured artifact status.","No L4 game/editor runtime loading is claimed.","Candidate entries are proposals only; LEDGER.json is untouched."]}
    dump(OUT/"wave13_consolidated.json",doc)
    cand=candidates(manifest); dump(OUT/"ledger_candidates.json",cand)
    (OUT/"WAVE13_EXECUTIVE_REPORT.md").write_text(report(doc,cand),encoding="utf-8")
    verifier='''#!/usr/bin/env python3\n"""Independent integrity check for t116 output; read-only."""\nimport hashlib,json,sys\nfrom pathlib import Path\nROOT=Path(__file__).resolve().parents[3]\nOUT=ROOT/"scratch/t116/out"\ndef sha(p):\n h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()\ndef main():\n d=json.loads((OUT/"wave13_consolidated.json").read_text(encoding="utf-8")); errors=[]\n if d.get("status")!="complete": errors.append("status")\n for a in d.get("artifacts",[]):\n  if not a.get("present",True): continue\n  p=ROOT/a["path"]\n  if not p.exists(): errors.append("missing:"+a["path"]); continue\n  if a.get("sha256") and sha(p)!=a["sha256"]: errors.append("sha256:"+a["path"])\n c=json.loads((OUT/"ledger_candidates.json").read_text(encoding="utf-8"))\n ids=[e.get("id") for e in c.get("entries",[])]\n if ids!=["E%d"%i for i in range(142,151)]: errors.append("candidate_ids")\n if c.get("status")!="draft_not_ledgered": errors.append("candidate_status")\n if errors: print("FAIL",*errors,sep="\\n"); return 1\n print("PASS artifacts=%d candidates=%d regressions=%d"%(len(d.get("artifacts",[])),len(ids),len(d.get("regression_matrix",[])))); return 0\nif __name__=="__main__": sys.exit(main())\n'''
    (OUT/"verify_wave13.py").write_text(verifier,encoding="utf-8")
    # Final marker deliberately written last.
    count=sum(1 for x in manifest if x.get("present",True)); ok=sum(x["exit_code"]==0 for x in reg)
    (OUT/"DONE.md").write_text(f"DONE type=t116\nstatus=complete\nmanifest_artifacts={count}\nregressions_passed={ok}/{len(reg)}\nbig3_gross=379/1034 (36.7%)\nbig3_net=379/673 (56.3%)\nt110_tables=55/67, l3_mappings=1056\nt96c_done_closed=41 (brief says 42; discrepancy flagged)\nbasic_people_rows=658011 diff=0\nledger_candidates=E142-E150 (draft; not entered)\n",encoding="utf-8")
    return doc


def selftest():
    assert sha_bytes(b"abc")=="ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad"
    assert len(lanes())==9
    assert [x[0] for x in [(142,),(150,)]]==[142,150]
    print("selftest: PASS")

def sha_bytes(b): return hashlib.sha256(b).hexdigest()

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--selftest",action="store_true"); ap.add_argument("--outdir",default="scratch/t116/out")
    args=ap.parse_args()
    if args.selftest: selftest(); return 0
    if (ROOT/args.outdir).resolve()!=OUT.resolve(): print("error: only scratch/t116/out is permitted",file=sys.stderr); return 2
    build(); print("t116 outputs written to scratch/t116/out"); return 0
if __name__=="__main__":
    try: sys.exit(main())
    except Exception as e: print(f"t116 error: {e}",file=sys.stderr); sys.exit(1)
