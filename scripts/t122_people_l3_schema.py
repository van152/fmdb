#!/usr/bin/env python3
"""Build range-aware person wire/IDA schema from t120 and t118 evidence."""
import json, argparse
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'scratch/t122/out'
TRACES=ROOT/'scratch/t120/out/people_unicorn_traces.json'
MAP=ROOT/'scratch/t118/out/people_4cc_mem.json'
OFFSETS={'1':0xf8,'2':0x278,'3':0x368,'4':0x138,'5':0}

def hx(v):
    try:return int(v,0)
    except (TypeError,ValueError):return None

def classify(p,w,n):
    if p=='2':
        if w<10:return 'PLAYER CA/PA/reputation fixed header'
        if 29<=w and w+n<=98:return 'PLAYER_DATA 69-byte attribute block (unnamed bytes absent 4CC proof)'
        if w<148:return 'PLAYER fixed header/date/physical fields (IDA callsite required for semantic label)'
        return 'PLAYER trailing/sub-object/identity region'
    if p=='1':return 'NON_PLAYER subclass body / embedded object (see reader callsite)'
    if p=='3':return 'ACTUAL_PLAYER_AND_NON_PLAYER subclass body / embedded object'
    if p=='4':return 'OFFICIAL subclass body / embedded object'
    return 'RETIRED_PERSON compact body / identity fields'

def build():
    t=json.loads(TRACES.read_text(encoding='utf-8')); m=json.loads(MAP.read_text(encoding='utf-8'))
    maps=[x for x in m['mappings'] if x.get('class_name') in ('PERSON','CONTRACT','BASIC_PERSON') and x.get('mem_off')]
    bytype={}; joined_global={}; wire_fields=[]
    for typ, samples in t['samples_by_type'].items():
        vb=OFFSETS[typ]; allreads=[]; joins={}
        for sample in samples:
            for r in sample['reads']:
                x=dict(r); x['classification']=classify(typ,r['wire_pos'],r['n']); allreads.append(x)
                if r.get('dst_kind')!='obj_mem':continue
                start=hx(r.get('base_off'))-vb
                if start is None:continue
                end=start+r['n']
                for q in maps:
                    off=hx(q['mem_off']); width=q.get('width')
                    if off is None or not width:continue
                    if off<end and off+width>start:
                        key=(q['class_name'],q['fourcc'],q['mem_off'],width)
                        joins[str(key)]={'class_name':q['class_name'],'fourcc':q['fourcc'],'mem_off':q['mem_off'],'width':width,'type':q.get('type'),'access_kind':q.get('access_kind'),'source':q.get('source'),'join_overlap':[max(start,off),min(end,off+width)],'evidence_level':'L3: Unicorn obj_mem range + t118 IDA 4CC/mem_off'}
        bytype[typ]={'class':t['type_stats'][typ]['class'],'rows':t['type_stats'][typ]['rows_ok'],'obj_offset_from_base':hex(vb),'sample_count':len(samples),'sample_reads':allreads,'joined_4ccs':list(joins.values()),'joined_4cc_count':len(joins)}
        joined_global[typ]=len(joins)
        if typ=='2':
            # Union observed fields by wire start, preserving disagreements as samples.
            grouped={}
            for s in samples:
                for r in s['reads']:
                    if r['wire_pos']>=148:continue
                    k=(r['wire_pos'],r['n']); grouped.setdefault(k,[]).append(r)
            for (pos,n),rs in sorted(grouped.items()):
                r=rs[0]; wire_fields.append({'wire_start':pos,'wire_end_exclusive':pos+n,'width':n,'base_off':r.get('base_off'),'obj_off':r.get('obj_off'),'classification':classify('2',pos,n),'caller_va':r.get('caller'),'sample_observations':len(rs),'hex_examples':[a['hex'] for a in rs[:3]],'evidence_level':'Unicorn-wire-verified; semantic name only where cited'})
    byte_map=[]
    for pos in range(148):
        covering=[f for f in wire_fields if f['wire_start']<=pos<f['wire_end_exclusive']]
        if covering:
            f=covering[0]; delta=pos-f['wire_start']; bo=hx(f['base_off']); oo=hx(f['obj_off'])
            byte_map.append({'wire_offset':pos,'base_off':hex(bo+delta) if bo is not None else None,'obj_off':hex(oo+delta) if oo is not None else None,'read_width':f['width'],'classification':f['classification'],'verified':True})
        else:byte_map.append({'wire_offset':pos,'base_off':None,'obj_off':None,'read_width':None,'classification':'no sampled read at this byte','verified':False})
    result={'schema_id':'fm24.t122.people_l3_schema','schema_version':1,'evidence':{'traces':str(TRACES.relative_to(ROOT)),'mapping':str(MAP.relative_to(ROOT)),'ida_readers':'scratch/t120/out/funcs/*.c; t113 sources cited per mapping'},'type_stats':t['type_stats'],'virtual_base_offsets':{t['factory'][k]['class']:hex(v) for k,v in OFFSETS.items()},'person_types':bytype,'player_wire_0_147':{'scope':'wire offsets 0..147, end-exclusive 148','fields':wire_fields,'byte_map':byte_map,'note':'Exact per-byte destination map is included; gaps mean no sampled read was found. Exact field naming must be based on C/source evidence, not inferred from bytes.'},'fourcc_join_count_by_type':joined_global,'fourcc_join_policy':'Map mem_off into most-derived object coordinates as base_off - obj_offset_from_base; only numeric mem_off and width ranges can join. Helper-only mappings are excluded.'}
    return result

def selftest(d):
    assert len(d['person_types'])==5
    assert d['person_types']['2']['class']=='PLAYER'
    assert d['virtual_base_offsets']['PLAYER']=='0x278'
    fields=d['player_wire_0_147']['fields']
    assert any(x['wire_start']==0 and x['width']==10 for x in fields)
    assert any(x['wire_start']==29 and x['width']==69 for x in fields)
    assert all('obj_offset_from_base' in x for x in d['person_types'].values())
    return True

def report(d):
    lines=['# t122 — people_db.dat Full L3 Schema','',f"Evidence rows: {sum(x['rows_ok'] for x in d['type_stats'].values()):,}; samples: {sum(v['sample_count'] for v in d['person_types'].values())}; overall 4CC mappings: {sum(d['fourcc_join_count_by_type'].values())} type-specific joins.",'','## Person types','','| Type | Class | Rows | Virtual base offset | Sample reads | Joined 4CCs |','|---:|---|---:|---:|---:|---:|']
    for k,v in d['person_types'].items():lines.append(f"| {k} | {v['class']} | {v['rows']} | {v['obj_offset_from_base']} | {sum(len(s['reads']) for s in json.loads(TRACES.read_text())['samples_by_type'][k])} | {v['joined_4cc_count']} |")
    lines+=['','## PLAYER wire 0..147 (end-exclusive 148)','','| Wire | Bytes | base_off | obj_off | Classification | Evidence |','|---:|---:|---|---|---|---|']
    for f in d['player_wire_0_147']['fields']:lines.append(f"| {f['wire_start']}..{f['wire_end_exclusive']-1} | {f['width']} | {f['base_off']} | {f['obj_off']} | {f['classification']} | Unicorn trace; {f['sample_observations']} observations |")
    lines+=['','### 69-byte PLAYER_DATA region','','Wire bytes 29..97 inclusive are read as a single 69-byte block into `obj_off=-0x70` (`base_off=0x208` in the supplied representative trace). Available 4CC joins are reported separately in JSON; no PDxx/Pxxx labels are asserted without a matching numeric `mem_off` and C evidence.','', '## Evidence levels','','- **L3-joined:** observed Unicorn object-memory range overlaps an IDA 4CC mapping with numeric offset and width.','- **Unicorn-wire-verified:** exact wire width and destination offset are observed; no 4CC semantic join is claimed.','- **Static-only:** code/source claims are not promoted to runtime field semantics.','', '## Caveats','','Range join uses `base_off - obj_offset_from_base` to express reads relative to each dynamic type. Pointer/helper-only 4CCs cannot be range-joined. Sample reads are preserved in JSON.','']
    return '\n'.join(lines)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--selftest',action='store_true');a=ap.parse_args(); OUT.mkdir(parents=True,exist_ok=True)
    d=build()
    if a.selftest:
        selftest(d);print('t122 selftest: PASS');return
    (OUT/'people_l3_schema.json').write_text(json.dumps(d,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
    (OUT/'REPORT.md').write_text(report(d),encoding='utf-8')
    assert selftest(d)
    done=['DONE type=t122','',f"Rows walked: {sum(x['rows_ok'] for x in d['type_stats'].values()):,}; type-specific joined 4CC count sum: {sum(d['fourcc_join_count_by_type'].values())}.", 'Verified PLAYER wire chunks before byte 148: '+str(len(d['player_wire_0_147']['fields']))+'.','Selftest: PASS (run `py -V:3.12 -B scripts/t122_people_l3_schema.py --selftest`).','Deliverables: `scripts/t122_people_l3_schema.py`, `scratch/t122/out/people_l3_schema.json`, `scratch/t122/out/REPORT.md`, `scratch/t122/out/DONE.md`.','']
    (OUT/'DONE.md').write_text('\n'.join(done),encoding='utf-8')
    print('\n'.join(done))
if __name__=='__main__':main()
