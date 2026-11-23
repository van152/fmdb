import json,sys
sys.stdout.reconfigure(encoding='utf-8')
m=json.loads(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8').read())
print('keys',list(m.keys())[:20])
def find(o,path=''):
    if isinstance(o,dict):
        for k,v in o.items(): yield from find(v,path+'/'+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o): yield from find(v,path+'[%d]'%i)
    else:
        if isinstance(o,str) and o in ('nhrl','dbnm','Nnam','Nsnm','N3ln','Nnty','ttcl','tbcl'):
            yield path,o
seen=set()
for p,v in find(m):
    if v not in seen:
        seen.add(v); print(v,p)
