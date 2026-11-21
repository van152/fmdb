import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads(open('reports/club_nation_subtable_schema.json',encoding='utf-8').read())
t=d['nation_t9_wire']
print(json.dumps({k:v for k,v in t.items() if k not in ('table_9','table_extra_9')},ensure_ascii=False)[:1500])
print()
print('=== table_extra_9')
print(json.dumps(t['table_extra_9'],ensure_ascii=False)[:2500])
