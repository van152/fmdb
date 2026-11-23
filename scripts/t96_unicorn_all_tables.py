"""t96: batch Unicorn wire tracing of indexed FM24 database tables."""
from __future__ import annotations
import argparse, importlib.util, json, struct, sys, traceback
from collections import Counter
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"scratch/t96/out"; INDEX=ROOT/"scratch/t95/vtable_index.json"
def load_module():
 p=ROOT/"scripts/t95_unicorn_trace.py"; s=importlib.util.spec_from_file_location("t95_unicorn_trace",p); m=importlib.util.module_from_spec(s); sys.modules[s.name]=m; s.loader.exec_module(m); return m
def save(out, records, status="partial"):
 (out/"wire_traces.json").write_text(json.dumps({"status":status,"tables":records},separators=(",",":")),encoding="utf-8")
def run(pe,out):
 out.mkdir(parents=True,exist_ok=True); m=load_module(); emu=m.EditorEmulator(pe); raw_tables=json.loads(INDEX.read_text(encoding="utf-8"))["tables"]
 # The index contains multiple vtables for several table ids; use the first canonical entry per file id.
 tables=[]; table_ids=set()
 for item in raw_tables:
  tid=int(item["table_type"])
  if tid not in table_ids: tables.append(item); table_ids.add(tid)
 # Resume usable earlier records, collapsing duplicate keys to their latest state.
 records=[]; seen={}
 old=out/"wire_traces.json"
 if old.exists():
  try:
   for r in json.loads(old.read_text(encoding="utf-8")).get("tables",[]):
    k=(r.get("archive"),r.get("table_id"))
    # Keep resumable summary compact; preserve representative fields and errors.
    if isinstance(r.get("canonical_fields"),list):
     r["canonical_fields"]=r["canonical_fields"][:100]
     for f in r["canonical_fields"]:
      if isinstance(f.get("seen_in_rows"),list): f["seen_in_rows"]=f["seen_in_rows"][:100]
    if isinstance(r.get("row_lengths"),list) and int(r.get("total_rows_header",0))>500: r["row_lengths"]=r["row_lengths"][:100]
    k=(r.get("archive"),r.get("table_id")); seen[k]=r
  except Exception: pass
 closure={"status":"partial","tables":{}}
 for archive in ("server","client"):
  for t in tables:
   tid=int(t["table_type"]); key=(archive,tid)
   if key in seen and tid!=9: continue
   try: data=m.load_table_payload(archive,tid)
   except FileNotFoundError: continue
   if len(data)<22 or data[:2]!=b"\x03\x01":
    seen[key]={"archive":archive,"table_id":tid,"class":t["class"],"error":"invalid table header","all_rows_closed_to_footer":False}; save(out,list(seen.values())); continue
   version=struct.unpack_from("<H",data,6)[0]; count=struct.unpack_from("<I",data,8)[0]; func=t["slots_hex"][19 if archive=="server" else 20]
   footer=len(data)-9; pos=13; tested=ok=0; lengths=[]; callers=Counter(); fields={}; err=None; end_rip=None; un=[]; row0=None
   # Full execution for <=500 rows; bounded sample for large tables, as specified.
   limit=count if count<=500 else min(count,5)
   for row in range(limit):
    if pos>=footer: err=f"row {row}: reached footer before declared rows"; break
    res=emu.trace_read(int(func,0),data[pos:footer],version=version); tested+=1; end_rip=res["end_rip"]
    if not res["ok"] or not res["bytes_consumed"]:
     err=f"row {row}: {res['error'] or 'no progress'}"; un=res["unhandled_calls"]; break
    n=res["bytes_consumed"]
    if pos+n>footer: err=f"row {row}: overran footer"; break
    if row==0: row0=n
    lengths.append(n); ok+=1
    for ri,r in enumerate(res["reads"]):
     caller=r.get("caller"); callers[caller]+=1
     ident=(ri,r["wire_pos"],r["n"],r.get("dst_kind"),r.get("obj_off"),caller)
     f=fields.get(ident)
     if f is None: f=fields[ident]={"idx":len(fields),"wire_off_example":r["wire_pos"],"n":r["n"],"dst_kind":r.get("dst_kind"),"obj_off":r.get("obj_off"),"caller_va":caller,"variable_len":False,"seen_in_rows":[]}
     if row not in f["seen_in_rows"]: f["seen_in_rows"].append(row)
    pos+=n
   closed=count==0 or (ok==count and pos==footer)
   # Leading sentinel evidence is reported separately; it remains included in the executed wire bytes.
   pref=1 if data[13:14]==b"\x00" else 0
   rec={"archive":archive,"table_id":tid,"class":t["class"],"func_va":func,"version":version,"total_rows_header":count,"rows_tested":tested,"rows_ok":ok,"all_rows_closed_to_footer":closed,"row_prefix_bytes":pref,"row0_consumed_bytes":row0,"canonical_fields":list(fields.values()),"footer_offset":footer,"end_offset":pos,"payload_len":len(data),"row_lengths":lengths,"helper_callers":dict(callers)}
   if err: rec.update(error=err,end_rip=end_rip,unhandled_calls=un)
   seen[key]=rec
   if tid==9:
    closure["tables"][archive]={"rows_header":count,"rows_tested":tested,"rows_ok":ok,"row_lengths":lengths,"helper_callers":dict(callers),"footer_offset":footer,"end_offset":pos,"closed":closed,"error":err}
    (out/"table9_251_closure.json").write_text(json.dumps(closure,indent=2),encoding="utf-8")
   save(out,list(seen.values()))
   print(f"{archive}/table_{tid}: {ok}/{limit} rows, footer_closed={closed}",flush=True)
 records=list(seen.values()); closed=[r for r in records if r.get("all_rows_closed_to_footer")]; failed=[r for r in records if not r.get("all_rows_closed_to_footer")]
 report=["# t96 — 全表 Unicorn Wire 追踪","",f"- 记录表数：{len(records)}；footer 闭合：{len(closed)}；未闭合/失败：{len(failed)}。","- 对行数 >500 的表仅执行前 5 行；其余按 header 计数全量执行。","- 闭合表："+(", ".join(f"{r['archive']}/table_{r['table_id']}" for r in closed) or "无"),"","## 失败诊断"]
 report += [f"- {r.get('archive')}/table_{r.get('table_id')} ({r.get('class','?')}): {r.get('error','未到 footer')}；rows={r.get('rows_ok')}/{r.get('total_rows_header')}，offset={r.get('end_offset')} footer={r.get('footer_offset')}" for r in failed]
 report += ["","## table_9 闭包",""]
 for a,x in closure["tables"].items(): report.append(f"- {a}: {x['rows_ok']}/{x['rows_header']}，offset={x['end_offset']}/{x['footer_offset']}，closed={x['closed']}，helper callers={len(x['helper_callers'])}。")
 (out/"REPORT.md").write_text("\n".join(report)+"\n",encoding="utf-8")
 complete=all(r.get("all_rows_closed_to_footer") for r in records) and len(records)>=35
 save(out,records,"complete" if complete else "partial")
 if complete: (out/"DONE.md").write_text(f"DONE type=t96\n\n- 表记录：{len(records)}\n- footer 闭合：{len(closed)}\n",encoding="utf-8")
 return len(records),len(closed),complete

def main():
 ap=argparse.ArgumentParser(description=__doc__); ap.add_argument("--pe",type=Path,default=Path(r"D:\tmp2b\fm24\input\editor.exe")); ap.add_argument("--outdir",type=Path,default=OUT); ap.add_argument("--selftest",action="store_true"); a=ap.parse_args()
 try:
  if a.selftest:
   m=load_module(); e=m.EditorEmulator(a.pe); d=m.load_table_payload("server",45); v=struct.unpack_from("<H",d,6)[0]; r=e.trace_read(0x141544130,d[13:-9],version=v); print(f"selftest ok={r['ok']} consumed={r['bytes_consumed']}"); return 0 if r["ok"] and r["bytes_consumed"] else 1
  n,c,done=run(a.pe,a.outdir); print(f"OUTDIR={a.outdir} tables={n} footer_closed={c} status={'complete' if done else 'partial'}"); print("交付清单：wire_traces.json, table9_251_closure.json, REPORT.md"+(", DONE.md" if done else "")); return 0 if done else 1
 except Exception as e: print(f"ERROR: {e}",file=sys.stderr); traceback.print_exc(); return 1
if __name__=="__main__": raise SystemExit(main())
