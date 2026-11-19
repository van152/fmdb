import json
m=json.load(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8'))
for e in m['entities']['award.xml']:
    for f in e.get('fields',[]):
        if f.get('field')=='AWsh':
            print("AWsh:", f.get('name'))
            for sf in (f.get('list_item_fields') or []):
                print(f"   {sf.get('field'):6s} {str(sf.get('name'))[:40]:42s} {sf.get('type'):28s} {sf.get('database_table_type') or ''} {sf.get('min_value')} {sf.get('max_value')}")
