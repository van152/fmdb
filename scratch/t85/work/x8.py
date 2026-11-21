import json,sys
sys.stdout.reconfigure(encoding='utf-8')
for p in ('scratch/t25/out/cursor_nation.json','scratch/t25/out/rows_nation.json'):
    try: d=json.loads(open(p,encoding='utf-8').read())
    except Exception as e: print(p,'ERR',e); continue
    print('==',p,type(d).__name__,list(d.keys())[:12] if isinstance(d,dict) else len(d))
    s=json.dumps(d,ensure_ascii=False)
    print(s[:800])
