import json,sys
sys.stdout.reconfigure(encoding='utf-8')
m=json.loads(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8').read())
e=m['entities']['alternative names.xml'][0]
print(json.dumps(e,ensure_ascii=False,indent=1)[:2000])
print()
print('---- ntts')
for name,ent in m['entities'].items():
    for i,f in enumerate(ent[0]['fields'] if isinstance(ent,list) else []):
        if f['field']=='ntts': print('FOUND',name,i,json.dumps(f,ensure_ascii=False)[:600])
