import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads(open('reports/t22_nation_capital.json',encoding='utf-8').read())
print(list(d.keys()))
for k,v in d.items():
    if isinstance(v,list): print(k,len(v),json.dumps(v[:2],ensure_ascii=False)[:500])
    else: print(k,json.dumps(v,ensure_ascii=False)[:300])
