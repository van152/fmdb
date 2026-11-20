import json, itertools
d=json.load(open('evidence/fm24/reports/dbdat_decode/db_tables_small.json',encoding='utf-8'))
print(list(d)[:10])
def walk(o,path=''):
    if isinstance(o,dict):
        for k,v in o.items(): walk(v,path+'/'+str(k))
    elif isinstance(o,list):
        for i,v in enumerate(o[:2]): walk(v,path+f'[{i}]')
    else:
        pass
for k in list(d):
    v=d[k]
    print('KEY',k,type(v),len(v) if hasattr(v,'__len__') else '')
