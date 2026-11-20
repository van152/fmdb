import json
d=json.load(open('scratch/t74/_stats_a.json'))
print(json.dumps({k:{kk:v[kk] for kk in v if kk!='hist'} for k in d for v in [d[k]]},ensure_ascii=False,indent=1))
