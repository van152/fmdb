import json,sys
sys.stdout.reconfigure(encoding='utf-8')
m=json.loads(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8').read())
f=m['entities']['nation.xml'][0]['fields']
for i,x in enumerate(f[:40]):
    print(i,x['field'],'|',x.get('name'),'|',x.get('type'),'|',{k:v for k,v in x.items() if k.startswith('is_')})
