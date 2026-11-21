import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads(open('reports/club_nation_subtable_schema.json',encoding='utf-8').read())
for k in ('nation_data_side_status','nation_t9_wire','comp_collections'):
    v=d[k]
    print('==',k,list(v.keys()))
    print(json.dumps(v,ensure_ascii=False)[:1200])
    print()
