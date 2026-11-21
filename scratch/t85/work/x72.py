import json,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_client_extra_9.rows.jsonl',encoding='utf-8')]
items=[]
for r in rows:
    b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']; t=b[8+nl:]
    n=t[6]
    for k in range(n):
        items.append(t[8+27*k:8+27*(k+1)])
print('items',len(items))
for off in range(27):
    vals=collections.Counter(it[off] for it in items)
    d=len(vals)
    if d<=6: print(f'  byte+{off:2d} distinct={d} {vals.most_common(6)}')
    else: print(f'  byte+{off:2d} distinct={d} (high)')
