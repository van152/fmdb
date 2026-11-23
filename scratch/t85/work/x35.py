import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads(open('scratch/t72/out/fingerprints.json',encoding='utf-8').read())
s=d['tables']['nation']['slots'][23]
print(json.dumps(s,ensure_ascii=False)[:2500])
