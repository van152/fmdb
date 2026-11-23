import json,sys
sys.stdout.reconfigure(encoding='utf-8')
m=json.load(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8'))
nat=m['nation'] if isinstance(m,dict) and 'nation' in m else None
print(type(m), list(m.keys())[:6])
def find(o,key,path=''):
    if isinstance(o,dict):
        for k,v in o.items():
            if k==key: yield path+'/'+k, v
            else: yield from find(v,key,path+'/'+k)
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from find(v,key,f'{path}[{i}]')
for p,v in find(m,'Nnam'): print(p,'->',json.dumps(v,ensure_ascii=False)[:300])
