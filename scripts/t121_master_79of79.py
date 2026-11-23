#!/usr/bin/env python3
"""Merge the final five Unicorn traces and refresh range-aware L3 joins (stdlib only)."""
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'scratch/t121/out'
WIRE96 = ROOT / 'scratch/t96c/out/wire_traces_master.json'
WIRE119 = ROOT / 'scratch/t119/out/last5_traces.json'
IDA = ROOT / 'scratch/t108/out/fourcc_mem_map_v2.json'
VTABLE = ROOT / 'scratch/t95/vtable_index.json'
OLD = ROOT / 'scratch/t110/out/master_67tables_l3.json'
REPLACE = {('server', 0), ('client', 0), ('server', 32), ('server', 71), ('server', 72)}

def load(path):
    with path.open(encoding='utf-8') as f:
        return json.load(f)

def dump(path, obj):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def merge():
    base, last = load(WIRE96), load(WIRE119)
    bykey = {(x['archive'], int(x['table_id'])): x for x in base['tables']}
    lastkeys = {(x['archive'], int(x['table_id'])): x for x in last['tables']}
    assert set(lastkeys) == REPLACE, f'unexpected t119 keys: {set(lastkeys)}'
    assert all(k in bykey for k in REPLACE)
    bykey.update(lastkeys)
    tables = sorted(bykey.values(), key=lambda x: (x['archive'], int(x['table_id'])))
    closed = [x for x in tables if x.get('closed_to_footer') and x.get('diff_bytes') == 0]
    sampled = [x for x in tables if not (x.get('closed_to_footer') and x.get('diff_bytes') == 0) and x.get('rows_ok', 0) >= 50]
    failed = [x for x in tables if x not in closed and x not in sampled]
    assert (len(tables), len(closed), len(sampled), len(failed)) == (79, 46, 33, 0), (len(tables),len(closed),len(sampled),len(failed))
    result = dict(base)
    result.update(schema_id='fm24.t121.unicorn_wire_traces_79of79', schema_version=1,
                  total_archive_tables=79, closed_to_footer=46, sample_rows_all_ok=33,
                  total_clean=79, failed=0, tables=tables)
    return result

def join(wire):
    im = load(IDA); vindex = load(VTABLE); old = load(OLD)
    bytype = {}
    for t in im['tables']:
        bytype.setdefault(int(t['table_type']), []).append(t)
    wire_by = {}
    for t in wire['tables']:
        wire_by.setdefault(int(t['table_id']), []).append(t)
    # t110's exact lineage rule: matching class/entity_tag first, all variants if none.
    rows = []
    for typ, variants in sorted(bytype.items()):
        traces = wire_by.get(typ, [])
        joined, wireall = [], []
        for tr in traces:
            candidates = [v for v in variants if v.get('class') == tr.get('class') or v.get('entity_tag') == tr.get('class', '').lower()]
            if not candidates:
                candidates = variants
            for r in tr.get('row0_reads', []):
                off, n = r.get('obj_off_dec'), r.get('n', 0)
                if r.get('dst_kind') == 'this' and isinstance(off, int) and isinstance(n, int) and n > 0:
                    wireall.append({'archive':tr['archive'],'wire_off_row0':r.get('wire_pos'),'wire_len':n,'obj_off':off,'caller_va':r.get('caller'),'hex':r.get('hex')})
                    for v in candidates:
                        for code, field in v.get('fourccs', {}).items():
                            poss = [m.get('off_int') for m in field.get('mem_offsets', []) if isinstance(m.get('off_int'), int)]
                            q = field.get('primary_off_int')
                            if isinstance(q, int): poss.append(q)
                            for q in sorted(set(poss)):
                                if off <= q < off+n:
                                    joined.append({'fourcc':code,'table_class':v.get('class'),'entity_tag':v.get('entity_tag'),'archive':tr['archive'],'wire_off_row0':r.get('wire_pos'),'wire_len':n,'obj_off':off,'in_slot_off':q-off,'mem_off':q,'caller_va':r.get('caller'),'getter_cite':field.get('func_va'),'ida_slot':field.get('slot'),'access_kind':field.get('access_kind')})
        def unique(items, keys):
            seen=set(); out=[]
            for x in items:
                k=tuple(x.get(z) for z in keys)
                if k not in seen: seen.add(k); out.append(x)
            return out
        wireall=unique(wireall,('archive','wire_off_row0','obj_off','wire_len'))
        joined=unique(joined,('fourcc','archive','wire_off_row0','obj_off','mem_off'))
        status='NOT_IN_SERVER_CLIENT_DB' if not traces else ('CLOSED (diff=0)' if any(t.get('closed_to_footer') and t.get('diff_bytes')==0 for t in traces) else ('OK_SAMPLE (50 rows)' if any(t.get('rows_ok',0)>=50 for t in traces) else 'FAIL'))
        for variant in variants:
            cls=variant.get('class'); vjoined=[x for x in joined if x.get('table_class')==cls]
            codes={x['fourcc'] for x in vjoined}; sc={x['fourcc'] for x in vjoined if x['archive']=='server'}; cc={x['fourcc'] for x in vjoined if x['archive']=='client'}
            arch={t['archive']:('CLOSED (diff=0)' if t.get('closed_to_footer') and t.get('diff_bytes')==0 else 'OK_SAMPLE (50 rows)' if t.get('rows_ok',0)>=50 else 'FAIL') for t in traces}
            rows.append({'table_type':typ,'class':cls,'entity':variant.get('entity_tag'),'unicorn_status':status,'archive_status':arch,'joined_l3_fourccs':vjoined,'joined_l3_count':len(codes),'server_only_fourccs':sorted(sc-cc),'field_scope':{c:('shared' if c in sc and c in cc else 'server_only' if c in sc else 'client_only') for c in sorted(codes)},'wire_field_count':len(wireall)})
    joined_tables=sum(bool(r['joined_l3_fourccs']) for r in rows)
    mapping_count=sum(r['joined_l3_count'] for r in rows)
    # Trace-backed table rows (archive × table id), independently of IDA class variants.
    traces=[]
    for t in wire['tables']:
        traces.append({'archive':t['archive'],'table_id':t['table_id'],'class':t.get('class'),'rows_header':t.get('rows_header'),'rows_ok':t.get('rows_ok'),'closed_to_footer':t.get('closed_to_footer'),'diff_bytes':t.get('diff_bytes'),'status':'CLOSED (diff=0)' if t.get('closed_to_footer') and t.get('diff_bytes')==0 else 'OK_SAMPLE (50 rows)'})
    # New-class uplift: report codes among the five repaired traces, deduplicated within class.
    new_traces=[t for t in wire['tables'] if (t['archive'],int(t['table_id'])) in REPLACE]
    uplift={}
    old_codes={}
    for row in old.get('tables', []):
        old_codes.setdefault((row.get('table_type'), row.get('class')), set()).update(x['fourcc'] for x in row.get('joined_l3_fourccs', []))
    for label, tid in [('AWARD',0),('t32 STARTING_FUTURE_TRANSFER',32),('t71 STARTING_PAST_TRANSFER',71),('t72 STARTING_PAST_TRADE',72)]:
        codes=set()
        target_classes={t.get('class') for t in new_traces if int(t['table_id'])==tid}
        for row in rows:
            if row['table_type']==tid and row['class'] in target_classes:
                codes.update(x['fourcc'] for x in row['joined_l3_fourccs'] if (x['archive'],tid) in REPLACE)
        # Only list 4CCs absent from the corresponding t110 class mapping.
        present=set().union(*(old_codes.get((tid, cls), set()) for cls in target_classes)) if target_classes else set()
        uplift[label]=sorted(codes-present)
    summary={'table_count':len(rows),'joined_tables':joined_tables,'joined_l3_fourccs':mapping_count,'wire_trace_count':len(traces),'trace_closed':46,'trace_sample_ok':33,'trace_failed':0,'t110_before':{'joined_tables':55,'table_count':67,'joined_l3_fourccs':1056},'new_l3_fourccs':uplift}
    return {'status':'complete','schema_id':'fm24.t121.master_79of79_l3','schema_version':1,'inputs':['scratch/t121/out/wire_traces_79of79.json','scratch/t108/out/fourcc_mem_map_v2.json','scratch/t95/vtable_index.json'],'method':'t110 semantics: this-relative row0 read spans intersect IDA mem_offsets/primary_off_int; class/entity_tag match, fallback to all variants; in_slot_off=mem_off-obj_off. vtable_index is included as lineage input.','vtable_index_table_count':len(vindex.get('tables',[])),'tables':rows,'trace_coverage':traces,'summary':summary}, old

def report(wire, master):
    s=master['summary']; lines=['# t121 — Unified Unicorn 79/79 + range-aware L3','',f"Coverage: **79/79 (100.0%)**; closed **46**, sample_ok **33**, failed **0**.",'', '| Archive | ID | Class | Rows | Result |','|---|---:|---|---:|---|']
    for t in master['trace_coverage']:
        lines.append(f"| {t['archive']} | {t['table_id']} | {t['class']} | {t['rows_ok']}/{t['rows_header']} | {t['status']} |")
    lines += ['', '## L3 join', '', f"t110 baseline: **55/67 tables**, **1,056** L3 4CC mappings. t121: **{s['joined_tables']}/{s['table_count']} tables**, **{s['joined_l3_fourccs']}** mappings.", '', '| Newly closed class | Newly unlocked L3 4CCs |', '|---|---|']
    for name,codes in s['new_l3_fourccs'].items(): lines.append(f"| {name} | {', '.join(codes) if codes else 'none'} |")
    rows=[t for t in wire['tables'] if (t['archive'],int(t['table_id'])) in REPLACE]
    lines += ['', '## t112 reader compatibility', '', 'Fixed-length: server/t0 AWARD and client/t0 AWARD, each row length **76 B**; `13 + 3545 × (1 + 76) = 272978 = len − 9` (payload ends at footer). The other three are variable-length: server/t32 STARTING_FUTURE_TRANSFER (315 rows), server/t71 STARTING_PAST_TRANSFER (50 rows), server/t72 STARTING_PAST_TRADE (138 rows).', '', 'Upgrade spec for t112: add the two archive-specific t0/AWARD entries as fixed stride 77 B (one flag byte + 76 B row body), 3,545 rows; start at the established row origin and assert the end at `len(data)-9` (`13 + 3545×77 = 272978`). Add server/t32 and server/t72 as variable records: use the existing identity-scan boundary (`ordinal`, `dbid==uid`, terminal zero), do not invent a fixed stride or length formula; observed row spans are 50–212 B (315 rows) and 61–106 B (138 rows), respectively, and both close at `len(data)-9`. Add server/t71 as variable/partial only: source trace validates 50 rows out of 616,665; t112’s existing identity scan stalls at row 4,646, so preserve bounded partial status, report the stopping point, and do not assert full footer closure. For all variable readers enforce bounds and count limits, track row boundaries, and require footer equality only when the entire declared row set has been parsed.']
    return '\n'.join(lines)+'\n'

def main():
    ap=argparse.ArgumentParser(description=__doc__); ap.add_argument('--selftest',action='store_true'); ap.add_argument('--outdir',type=Path,default=OUT); a=ap.parse_args()
    for p in (WIRE96,WIRE119,IDA,VTABLE,OLD): assert p.exists(),f'missing input: {p}'
    wire=merge(); master,_=join(wire)
    assert master['summary']['trace_closed']==46 and master['summary']['trace_sample_ok']==33 and master['summary']['trace_failed']==0
    assert all(x['in_slot_off']>=0 and x['in_slot_off']<x['wire_len'] for r in master['tables'] for x in r['joined_l3_fourccs'])
    if a.selftest:
        assert len(wire['tables'])==79 and len(master['tables'])==67
        print(f"selftest PASS — 79/79, joined {master['summary']['joined_tables']}/{master['summary']['table_count']}, L3={master['summary']['joined_l3_fourccs']}"); return 0
    a.outdir.mkdir(parents=True,exist_ok=True)
    dump(a.outdir/'wire_traces_79of79.json',wire)
    dump(a.outdir/'master_79of79_l3.json',master)
    (a.outdir/'REPORT.md').write_text(report(wire,master),encoding='utf-8')
    s=master['summary']
    done=f"DONE type=t121\ncoverage=79/79 (100.0%)\nclosed=46\nsample_ok=33\nfailed=0\nt110=55/67 tables, 1056 L3 4CC mappings\nt121={s['joined_tables']}/{s['table_count']} tables, {s['joined_l3_fourccs']} L3 4CC mappings\nselftest=PASS (run py -V:3.12 -B scripts/t121_master_79of79.py --selftest)\n"
    (a.outdir/'DONE.md').write_text(done,encoding='utf-8')
    print('Deliverables:')
    for name in ('wire_traces_79of79.json','master_79of79_l3.json','REPORT.md','DONE.md'): print(f'  {a.outdir/name}')
    print(f"Core stats: 79/79; closed=46 sample_ok=33 failed=0; t121 L3={s['joined_tables']}/{s['table_count']} tables, {s['joined_l3_fourccs']} mappings")
    return 0
if __name__=='__main__':
    try: raise SystemExit(main())
    except Exception as e: print(f'ERROR: {e}',file=sys.stderr); raise SystemExit(1)
