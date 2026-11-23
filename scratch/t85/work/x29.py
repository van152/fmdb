import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads(open('reports/club_nation_subtable_schema.json',encoding='utf-8').read())
c=d['comp_collections']
for k in ('L3_grammar_slots','L3_reference_lane_bindings','held_reference_lane_records','held_slots','corrected_nonempty_rows','scope','status'):
    print(k,'=',json.dumps(c.get(k),ensure_ascii=False)[:700])
print()
print('grammar detail keys',[k for k in c if 'grammar' in k.lower() or 'slot' in k.lower()])
print(json.dumps(c.get('source_records') ,ensure_ascii=False)[:300] if 'source_records' in c else '')
