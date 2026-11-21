import json,sys
sys.stdout.reconfigure(encoding='utf-8')
m=json.loads(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8').read())
f=m['entities']['nation.xml'][0]['fields']
print('n fields',len(f))
for i in (6,7,8,11,12,18,19,221):
    print(i,json.dumps(f[i],ensure_ascii=False)[:400])
print()
print('entity meta',json.dumps({k:v for k,v in m['entities']['nation.xml'][0].items() if k!='fields'},ensure_ascii=False)[:500])
