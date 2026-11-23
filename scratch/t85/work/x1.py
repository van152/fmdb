import sys,json
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
d=C.jl('scratch/t75/out/xref_reverse.json')
# any 264 (0x108) as object displacement or in xrefs?
hits=[]
for s in d['slots']:
    if s.get('object_displacement')==264: hits.append((s['table'],s['slot'],'objdisp'))
    t=s.get('transfer') or {}
    if t.get('object_displacement')==264: hits.append((s['table'],s['slot'],'transfer'))
    for x in (s.get('displacement_xrefs_untyped') or [])[:0]: pass
print('0x108 as displacement:',hits)
# print structure of displacement_xrefs_untyped
s=d['slots'][0]
print('disp_xrefs sample',json.dumps(s.get('displacement_xrefs_untyped'),ensure_ascii=False)[:400])
print('reader_fragment',json.dumps(s.get('reader_fragment'),ensure_ascii=False)[:300])
print('selected_chain',json.dumps(s.get('selected_chain'),ensure_ascii=False)[:300])
print('codes',json.dumps(s.get('codes'),ensure_ascii=False)[:200])
print('grammar_ref',json.dumps(s.get('grammar_ref'),ensure_ascii=False)[:200])
