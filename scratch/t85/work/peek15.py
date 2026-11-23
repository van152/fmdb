import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads(open('reports/club_nation_subtable_schema.json',encoding='utf-8').read())
t=d['nation_t9_wire']['table_extra_9']
print(json.dumps(t.get('t50_data_side_candidate_profile'),ensure_ascii=False,indent=1)[:4000])
