import json,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
def L(p): return json.loads(open(p,encoding='utf-8').read())
inv=L('scratch/t72/out/inventory.json')
for ent in ('nation','comp'):
    e=inv['tables'][ent]
    print('==',ent,'table_id',e['table_id'],'nslots',len(e['slots']))
    print('kind_counts',e['kind_counts'])
    st=collections.Counter(s['slot_type'] for s in e['slots'])
    print('slot_types',st)
    coll=[s for s in e['slots'] if s['slot_type']=='collection']
    print('collections',len(coll))
    for s in coll:
        print('  pos',s['position'],'kind',s['kind'],'w',s['nominal_width'],'disp',s['object_displacement'],'cov',s['coverage'],json.dumps(s.get('collection'),ensure_ascii=False),'claims',s['claims'],'|',s.get('scope','')[:60])
    print('schema_attribution',json.dumps(e['schema_attribution'],ensure_ascii=False)[:400])
