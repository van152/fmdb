import json,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads(open('scratch/t64/out/field_map_r2.json',encoding='utf-8').read())
print(list(d.keys()))
f=d['fields']
print(len(f),list(f[0].keys()))
c=collections.Counter(x.get('classification') for x in f)
print(c)
for x in f:
    if x.get('classification')=='bounded_getter_without_wire_closure':
        print(json.dumps(x,ensure_ascii=False)[:340])
