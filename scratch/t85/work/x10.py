import json,sys,struct
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
rows={}
for p in ('table_client_9','table_server_9','table_client_extra_9','table_server_extra_9'):
    out=[]
    with open(f'scratch/t50/out/profiles/{p}.rows.jsonl',encoding='utf-8') as f:
        for line in f: out.append(json.loads(line))
    rows[p]=out
    print(p,len(out),'keys',list(out[0].keys()))
    print('  r0',json.dumps(out[0],ensure_ascii=False)[:300])
