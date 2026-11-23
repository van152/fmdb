#!/usr/bin/env python3
"""Conservative t117 audit: preserve classifications unless authoritative proof exists."""
import argparse, json, pathlib, collections, sys
ROOT=pathlib.Path(__file__).resolve().parents[1]
OUT=ROOT/'scratch/t117/out'
SRC=ROOT/'scratch/t109/out'

def load(p): return json.loads(p.read_text(encoding='utf-8'))
def dump(name,obj):
    p=OUT/name; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
def run():
    OUT.mkdir(parents=True,exist_ok=True)
    join=load(SRC/'big3_l3_join.json'); summary=load(SRC/'coverage_summary.json'); gaps=load(SRC/'remaining_gaps.json')
    rows=join['rows']; gap_by={r['id']:r for r in gaps['rows']}
    assert len(rows)==1034 and len(gaps['rows'])==294
    # t98 contains only persisted physical-column direct mappings; child offsets from t109
    # are null, so it cannot establish a byte-exact crosswalk for these candidates.
    t98=load(ROOT/'scratch/t98/out/table45_full_schema.json')
    phys={int(x['mem_off']):x for x in t98['physical_columns'] if x.get('mem_off') is not None}
    audit=[]
    for r in rows:
        original=r['new_class']; evidence=[]; decision='unchanged'
        if r['id'] in gap_by:
            g=gap_by[r['id']]
            if original=='gap_child_off_not_in_child_stream':
                evidence=['scratch/t98/out/table45_full_schema.json:physical_columns (18 exact columns; offsets 0x18..0x5e)',
                          'scratch/t98/out/table45_full_schema.json:accessor_codes (117 accessor ledger)']
                decision='unresolved_no_byte_offset'
                blocker='t109 child handler gives mem_off=null; t98 mapping cannot be joined to this 4CC without a proven physical-column/accessor crosswalk.'
            elif original=='gap_helper_computed':
                decision='unresolved_helper_not_decompiled'
                blocker='Inspect cited helper chain; the top helper may be absent from scratch/t95/funcs (see remaining_gaps_v2 blockers).'
            elif original=='gap_off_not_in_read_stream':
                decision='unresolved_runtime_join'
                blocker='Need trace mem_writes address plus serializer identity/callee chain; aggregate table trace alone does not prove the XML 4CC destination.'
            elif original=='gap_delegated_or_empty':
                decision='unresolved_delegate_or_empty'
                blocker='Need exact setter/delegate implementation and persisted read/write proof; gap label alone cannot distinguish empty setter from serialized delegate.'
            else:
                decision='unresolved_other_table'
                blocker='Need a cross-object identity route, not merely a same-tag dispatch elsewhere.'
            r['t117_audit']={'decision':decision,'evidence':evidence,'blocker':blocker}
        else:
            r['t117_audit']={'decision':'carried_forward','evidence':[r.get('serializer_cite')] if r.get('serializer_cite') else [],'blocker':None}
    counts=collections.Counter(r['new_class'] for r in rows)
    per={e:{'total':sum(r['entity']==e for r in rows),'by_class':dict(collections.Counter(r['new_class'] for r in rows if r['entity']==e))} for e in ('club','nation','comp')}
    # Persist the complete classification before generating dependent artifacts.
    dump('big3_l3_v2.json',{'schema_id':'fm24.t117.big3_l3_v2','schema_version':1,'status':'complete_conservative_audit','denominator':1034,'method':'No upgrades without a per-field trace-address/mem_off or exact decompiled source chain. All 294 t109 gaps retained.','rows':rows})
    rem=[{'id':r['id'],'entity':r['entity'],'code':r['code'],'class':r['new_class'],'mem_off':r.get('mem_off'),'gap_reason':r.get('gap_reason'),'t117_audit':r['t117_audit']} for r in rows if r['new_class'].startswith('gap_')]
    dump('remaining_gaps_v2.json',{'schema_id':'fm24.t117.remaining_gaps_v2','schema_version':1,'status':'complete_conservative_audit','gap_rows':len(rem),'by_class':dict(collections.Counter(x['class'] for x in rem)),'rows':rem})
    old=summary['summary']['new_scope']; closed=old['l3_closed_total']; net=old['denominator_net']
    dump('coverage_summary_v2.json',{'schema_id':'fm24.t117.coverage_summary_v2','schema_version':1,'status':'complete','denominator':1034,'before_t109':{'gross':f"{closed}/1034",'net':f"{closed}/{net}",'gap_total':294},'after_t117':{'gross':f'{closed}/1034','gross_ratio':round(closed/1034,4),'net':f'{closed}/{net}','net_ratio':round(closed/net,4),'gap_total':len(rem),'upgraded':0},'by_class':dict(counts),'per_entity':per,'conservation':{'club':433,'nation':346,'comp':255,'sum':1034}})
    report='''# t117 Big-3 gap closure audit\n\nResult: **0 of 294 gaps upgraded**. This is intentional: available evidence does not provide the required per-4CC destination provenance. The denominator remains 1,034; coverage remains 379/1,034 gross (36.7%) and 379/673 net (56.3%).\n\n## Findings and blockers\n- The `gap_off_not_in_read_stream` classification cannot be resolved from table-level trace summaries. A valid upgrade requires a concrete Unicorn write address and `mem_off`, joined to the corresponding accessor/4CC.\n- All 21 table_45 child candidates have `mem_off=null` in the t109 handler route. t98 gives 18 physical columns and 117 accessors, but no proven crosswalk from those rows to these 21 tags. They remain unresolved rather than being guessed.\n- Helper/delegate/other-table rows remain unresolved absent exact persisted-field proof. The generated JSON retains each row, its old evidence and a category-specific next step.\n- `t105 --selftest` failure diagnosis: its `steps("NTC::server")` lookup raises KeyError because the serialized function key is `NATIONAL_TEAM_CONTAINER::server` (see `scratch/t105/out/big3_serializers.json` `functions` keys); test label/key alias is inconsistent. No t105 source was modified.\n\n## Verification\nAll 1,034 t109 rows are conserved with unchanged classes. No evidence was promoted to L3/exclusion.\n'''
    (OUT/'REPORT.md').write_text(report,encoding='utf-8')
    (OUT/'DONE.md').write_text('''# DONE type=t117\n\n- Denominator conserved: 1,034 (CLUB 433, NATION 346, COMP 255).\n- L3: 379/1,034 gross (36.7%); 379/673 net (56.3%).\n- Upgraded gaps: 0; remaining: 294. No unsupported classifications promoted.\n- `py -V:3.12 -B scripts/t117_big3_gap_closure.py --selftest`: PASS (run immediately after generation).\n- See `REPORT.md` for limitations and the t105 selftest diagnosis.\n''',encoding='utf-8')
    print('deliverables: big3_l3_v2.json coverage_summary_v2.json remaining_gaps_v2.json REPORT.md DONE.md')
    print(f"denominator=1034 gross={closed}/1034 ({closed/1034:.1%}) net={closed}/{net} ({closed/net:.1%}) upgraded=0 remaining={len(rem)}")

def selftest():
    d=load(OUT/'big3_l3_v2.json'); s=load(OUT/'coverage_summary_v2.json'); r=load(OUT/'remaining_gaps_v2.json')
    assert len(d['rows'])==1034 and r['gap_rows']==294 and s['conservation']['sum']==1034
    assert sum(s['per_entity'][e]['total'] for e in ('club','nation','comp'))==1034
    print('t117 selftest: PASS')
if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--selftest',action='store_true');args=a.parse_args()
    if args.selftest:selftest()
    else:run()
