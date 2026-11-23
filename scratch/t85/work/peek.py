import json,sys
sys.stdout.reconfigure(encoding='utf-8')
def L(p): return json.loads(open(p,encoding='utf-8').read())
inv=L('scratch/t72/out/inventory.json')
for ent in inv['tables']:
    e=inv['tables'][ent]
    print('==',ent,type(e).__name__, list(e.keys())[:12] if isinstance(e,dict) else len(e))
print()
n=inv['tables']['nation']
print(json.dumps(n,ensure_ascii=False)[:2000])
