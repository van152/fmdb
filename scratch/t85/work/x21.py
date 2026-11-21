import json,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_client_extra_9.rows.jsonl',encoding='utf-8')]
b=bytes.fromhex(rows[0]['raw_hex'])
for i in range(16,len(b)):
    print(f'{i:4d} 0x{i:02x} {b[i]:02x} {b[i]:3d}')
