import json,sys
sys.stdout.reconfigure(encoding='utf-8')
def L(p): return json.loads(open(p,encoding='utf-8').read())
f=L('scratch/t72/out/fingerprints.json')
print('keys',list(f.keys()))
t=f['tables']
print(type(t), list(t.keys())[:8] if isinstance(t,dict) else len(t))
print(json.dumps(f.get('grading_ceiling'),ensure_ascii=False)[:300])
n=t['nation'] if isinstance(t,dict) else None
print('nation keys',list(n.keys()) if isinstance(n,dict) else type(n))
print(json.dumps(n,ensure_ascii=False)[:1500])
