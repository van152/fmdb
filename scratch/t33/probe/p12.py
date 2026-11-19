import json
m=json.load(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8'))
def walk(fields,path,out):
    for f in fields:
        if f.get('type')=='list':
            out.append((path,f))
        if f.get('list_item_fields'):
            walk(f['list_item_fields'], path+'.'+str(f.get('field'))+'.item', out)
for fn,ents in m.get('entities',{}).items():
    for e in ents:
        out=[]; walk(e.get('fields',[]), f"{fn}#{e.get('id')}", out)
        for p,f in out:
            nm=str(f.get('name',''))
            if any(k in nm.upper() for k in ('RECORD','AWARD','POINT','MEDIA','WAGE')):
                print(f"{fn}#{e.get('id'):6s} {f.get('field')} | {nm} | items={len(f.get('list_item_fields') or [])}")
