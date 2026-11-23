#!/usr/bin/env python3
"""Build the t110 range-aware Unicorn/IDA L3 ledger. Python 3.12, stdlib only."""
import argparse, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'scratch/t110/out'
WIRE = ROOT / 'scratch/t96c/out/wire_traces_master.json'
IDA = ROOT / 'scratch/t108/out2/fourcc_mem_map_v2.json'
REG = ROOT / 'reports/club_nation_subtable_schema.json'

def load(p):
    with p.open(encoding='utf-8') as f: return json.load(f)
def hx(v):
    if isinstance(v, int): return v
    try: return int(str(v), 0)
    except (ValueError, TypeError): return None
def dump(p, obj):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def build():
    w=load(WIRE); im=load(IDA); regress=load(REG)
    bytype={}
    for t in im['tables']: bytype.setdefault(int(t['table_type']), []).append(t)
    wire_by={}
    for t in w['tables']: wire_by.setdefault(int(t['table_id']), []).append(t)
    rows=[]
    for typ, variants in sorted(bytype.items()):
        traces=wire_by.get(typ, [])
        # Pair trace/class with matching IDA lineage, retaining class merges.
        joined=[]; wireall=[]
        for tr in traces:
            reads=tr.get('row0_reads', [])
            # A trace is linked to each compatible IDA class; same physical offsets are deduplicated later.
            candidates=[v for v in variants if v.get('class')==tr.get('class') or v.get('entity_tag')==tr.get('class','').lower()]
            if not candidates: candidates=variants
            for r in reads:
                off=r.get('obj_off_dec'); n=r.get('n',0)
                if r.get('dst_kind')=='this' and isinstance(off,int) and isinstance(n,int) and n>0:
                    wireall.append({'archive':tr['archive'],'wire_off_row0':r.get('wire_pos'),'wire_len':n,'obj_off':off,'caller_va':r.get('caller'),'hex':r.get('hex')})
                    for v in candidates:
                        for code, field in v.get('fourccs',{}).items():
                            poss=[]
                            for mo in field.get('mem_offsets',[]):
                                q=mo.get('off_int')
                                if isinstance(q,int): poss.append(q)
                            q=field.get('primary_off_int')
                            if isinstance(q,int): poss.append(q)
                            # Derived subobject bases are included only when explicitly represented by mem_offsets.
                            for q in sorted(set(poss)):
                                if off <= q < off+n:
                                    joined.append({'fourcc':code,'table_class':v.get('class'),'entity_tag':v.get('entity_tag'),'archive':tr['archive'],'wire_off_row0':r.get('wire_pos'),'wire_len':n,'obj_off':off,'in_slot_off':q-off,'mem_off':q,'caller_va':r.get('caller'),'getter_cite':field.get('func_va'),'ida_slot':field.get('slot'),'access_kind':field.get('access_kind')})
        # Normalize wires and joined mappings; duplicate candidate lineage does not inflate counts.
        def unique(items, keys):
            seen=set(); out=[]
            for x in items:
                k=tuple(x.get(z) for z in keys)
                if k not in seen: seen.add(k); out.append(x)
            return out
        wireall=unique(wireall,('archive','wire_off_row0','obj_off','wire_len'))
        joined=unique(joined,('fourcc','archive','wire_off_row0','obj_off','mem_off'))
        server=[x for x in wireall if x['archive']=='server']; client=[x for x in wireall if x['archive']=='client']
        server_j=[x for x in joined if x['archive']=='server']; client_j=[x for x in joined if x['archive']=='client']
        allcodes={x['fourcc'] for x in joined}; sc={x['fourcc'] for x in server_j}; cc={x['fourcc'] for x in client_j}
        statuses=[]
        for tr in traces:
            if tr.get('closed_to_footer') and tr.get('diff_bytes')==0: statuses.append('CLOSED (diff=0)')
            elif tr.get('rows_ok',0)>=50: statuses.append('OK_SAMPLE (50 rows)')
            else: statuses.append('FAIL')
        status='NOT_IN_SERVER_CLIENT_DB' if not traces else ('CLOSED (diff=0)' if 'CLOSED (diff=0)' in statuses else ('OK_SAMPLE (50 rows)' if 'OK_SAMPLE (50 rows)' in statuses else 'FAIL'))
        for variant in variants:
            vclass=variant.get('class')
            vjoined=[x for x in joined if x.get('table_class')==vclass]
            vcodes={x['fourcc'] for x in vjoined}
            vsc={x['fourcc'] for x in vjoined if x['archive']=='server'}
            vcc={x['fourcc'] for x in vjoined if x['archive']=='client'}
            rows.append({'table_type':typ,'class':vclass,'entity':variant.get('entity_tag'),'unicorn_status':status,'archive_status':{t['archive']:('CLOSED (diff=0)' if t.get('closed_to_footer') and t.get('diff_bytes')==0 else 'OK_SAMPLE (50 rows)' if t.get('rows_ok',0)>=50 else 'FAIL') for t in traces},'server_wire_fields':server,'client_wire_fields':client,'joined_l3_fourccs':vjoined,'joined_l3_count':len(vcodes),'server_only_fourccs':sorted(vsc-vcc),'field_scope':{c:('shared' if c in vsc and c in vcc else 'server_only' if c in vsc else 'client_only') for c in sorted(vcodes)},'unmatched_wire_fields':[x for x in wireall if not any(j['archive']==x['archive'] and j['wire_off_row0']==x['wire_off_row0'] and j['obj_off']==x['obj_off'] for j in vjoined)]})
    # Compare pre-existing L3 field coordinates to physical wire spans (offsets are preserved as supplied).
    checks=[]
    for table in regress.get('tables',[]):
        typ=table.get('table_type'); row=next((r for r in rows if r['table_type']==typ),None)
        for f in table.get('fields',[]):
            if f.get('status')!='L3': continue
            target=f.get('wire_offset',f.get('row_offset')); width=f.get('width_bytes') or 1
            target=hx(target)
            spans=[] if row is None else row['server_wire_fields']+row['client_wire_fields']
            hit=next((x for x in spans if target is not None and x['obj_off']<=target<x['obj_off']+x['wire_len']),None)
            kind='mismatch' if not hit else 'exact' if hit['obj_off']==target else 'within_slot'
            checks.append({'table_type':typ,'entity':table.get('entity'),'fourcc':f.get('code'),'expected_offset':target,'width_bytes':width,'result':kind,'wire_off_row0':hit.get('wire_off_row0') if hit else None,'wire_obj_off':hit.get('obj_off') if hit else None,'reason':None if hit else 'No row0 Unicorn this-relative read span covers the accepted L3 coordinate; archive/path/coordinate semantics may differ.'})
    summary={'table_count':len(rows),'joined_tables':sum(bool(r['joined_l3_fourccs']) for r in rows),'joined_l3_fourccs':sum(r['joined_l3_count'] for r in rows),'server_wire_field_count':sum(len(r['server_wire_fields']) for r in rows),'client_wire_field_count':sum(len(r['client_wire_fields']) for r in rows),'regression':{'exact':sum(x['result']=='exact' for x in checks),'within_slot':sum(x['result']=='within_slot' for x in checks),'mismatch':sum(x['result']=='mismatch' for x in checks),'checks':checks}}
    master={'status':'complete','schema_id':'fm24.t110.master_l3','schema_version':1,'inputs':['scratch/t96c/out/wire_traces_master.json','scratch/t108/out2/fourcc_mem_map_v2.json'],'method':'this-relative Unicorn row0 read spans intersect IDA mem_off; in_slot_off=mem_off-obj_off','tables':rows,'summary':summary}
    coverage={'status':'complete','summary':summary,'table_coverage':[{'table_type':r['table_type'],'class':r['class'],'unicorn_status':r['unicorn_status'],'joined_l3_count':r['joined_l3_count'],'server_wire_fields':len(r['server_wire_fields']),'client_wire_fields':len(r['client_wire_fields'])} for r in rows]}
    return master,coverage

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--selftest',action='store_true'); ap.add_argument('--outdir',type=Path,default=OUT); a=ap.parse_args()
    if a.selftest:
        assert all(p.exists() for p in (WIRE,IDA,REG)), 'required source missing'
        m,c=build(); assert len(m['tables'])==67, f"expected 67 IDA tables, got {len(m['tables'])}"
        assert all(x['in_slot_off']>=0 and x['in_slot_off']<x['wire_len'] for r in m['tables'] for x in r['joined_l3_fourccs'])
        print('selftest PASS'); return 0
    m,c=build(); a.outdir.mkdir(parents=True,exist_ok=True)
    dump(a.outdir/'master_67tables_l3.json',m); dump(a.outdir/'coverage_milestone.json',c)
    print(f"Join tables={m['summary']['joined_tables']} L3 rows={m['summary']['joined_l3_fourccs']} regression exact/within_slot/mismatch={c['summary']['regression']['exact']}/{c['summary']['regression']['within_slot']}/{c['summary']['regression']['mismatch']}")
    return 0
if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as e: print(f'ERROR: {e}',file=sys.stderr); raise SystemExit(1)
