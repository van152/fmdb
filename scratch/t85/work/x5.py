import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads(open('scratch/t50/out/profile_t9.json',encoding='utf-8').read())
m=d['members']
print(type(m), list(m)[:6] if isinstance(m,dict) else len(m))
k=[x for x in m if 'extra' in x]
print(k)
print(json.dumps(m[k[0]] if k else None,ensure_ascii=False)[:2500])
