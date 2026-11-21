import json,sys
sys.stdout.reconfigure(encoding='utf-8')
def L(p): return json.loads(open(p,encoding='utf-8').read())
d=L('scratch/t75/out/xref_reverse.json')
print('=== nation_escalations (10)')
for e in d['nation_escalations']:
    print(json.dumps(e,ensure_ascii=False)[:600]); print()
