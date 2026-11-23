import json,sys
sys.stdout.reconfigure(encoding='utf-8')
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_client_extra_9.rows.jsonl',encoding='utf-8')]
b=bytes.fromhex(rows[0]['raw_hex'])
print('len',len(b))
for i in range(0,len(b),20):
    ch=b[i:i+20]
    print(f'{i:4d} {ch.hex(" "):60s} {"".join(chr(c) if 32<=c<127 else "." for c in ch)}')
