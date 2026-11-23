import json
d=json.load(open('evidence/fm24/reports/editor_schema/master.json'))
ents=d['entities']
print(type(ents), len(ents))
k=list(ents)[:5] if isinstance(ents,dict) else None
print(k)
for name in ('media','derby','weather','team','award','agreement','local_region','stadium','language'):
    if isinstance(ents,dict):
        found=[kk for kk in ents if name.lower() in kk.lower()]
        print(name,'->',found[:4])
