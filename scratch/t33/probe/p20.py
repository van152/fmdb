import json
m=json.load(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8'))
for fn in ('team.xml','player.xml','person.xml'):
    for e in m['entities'][fn]:
        def walk(fields,d=0):
            for f in fields:
                if f.get('type')=='list':
                    kids=f.get('list_item_fields') or []
                    print(f"  {fn}#{e.get('id'):4s} {f.get('field'):6s} {str(f.get('name'))[:36]:38s} items={len(kids)}")
                if f.get('list_item_fields'): walk(f['list_item_fields'],d+1)
        walk(e.get('fields',[]))
