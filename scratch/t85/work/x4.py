import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads(open('scratch/t50/out/profile_t9.json',encoding='utf-8').read())
print(list(d.keys()))
print(json.dumps({k:v for k,v in d.items() if 'extra' in k.lower()},ensure_ascii=False)[:3000])
