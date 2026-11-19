import json
m=json.load(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8'))
ent=m.get('entities',{})
print("entities:", list(ent)[:40])
def lists(entname):
    for e in ent.get(entname,[]):
        def walk(fields):
            for f in fields:
                if f.get('type')=='list':
                    yield f
                if f.get('list_item_fields'):
                    yield from walk(f['list_item_fields'])
        for f in walk(e.get('fields',[])):
            print(f"  {entname}#{e.get('id')} {f.get('field')} | {f.get('name')}")
for n in ('award.xml','comp.xml'):
    print("==",n); lists(n)
