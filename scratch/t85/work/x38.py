import json,sys
sys.stdout.reconfigure(encoding='utf-8')
d=json.loads(open('scratch/t25/out/cursor_nation.json',encoding='utf-8').read())
print(json.dumps(d['row_grammar'],ensure_ascii=False,indent=1)[:3000])
