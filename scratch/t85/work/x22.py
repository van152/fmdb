import json,sys
sys.stdout.reconfigure(encoding='utf-8')
m=json.loads(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8').read())
ent=m['entities']['nation.xml'][0]
print(json.dumps(ent['other_records'],ensure_ascii=False))
codes={f['field']:i for i,f in enumerate(ent['fields'])}
for c in ('alnm','ntts','TCnn','TCht','dbnm','Nnam','Nsnm','N3ln','Nnty','nhrl'):
    print(c,'idx',codes.get(c))
# search other entities for alnm as list entity
for name,e in m['entities'].items():
    for i,f in enumerate(e[0]['fields'] if isinstance(e,list) else []):
        if f['field'] in ('alnm','ntts'):
            print('FOUND',name,i,json.dumps(f,ensure_ascii=False)[:300])
