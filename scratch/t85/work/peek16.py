import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads(open('scratch/t75/out/xref_reverse.json',encoding='utf-8').read())
for s in d['slots']:
    fc=s.get('first_counterexample') or {}
    src=fc.get('source') if isinstance(fc,dict) else None
    print('%-10s %-8s %s | %s'%(s.get('table'),s.get('slot'),s.get('kind'),(src or str(fc))[:110]))
