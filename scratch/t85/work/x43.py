import json,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_client_extra_9.rows.jsonl',encoding='utf-8')]
# candidate struct offsets: after name there's u32 then 6B then a repeated pattern
# find all blocks sharing identical suffix grammar: dump row0 aligned 4-byte groups
b=bytes.fromhex(rows[0]['raw_hex'])
nl=rows[0]['marker']['name_len']
print('name_len',nl)
tail=b[8+nl:]
print('tail len',len(tail))
for i in range(0,len(tail),4):
    print(f'{i:3d} {tail[i:i+4].hex(" ")}  u32={int.from_bytes(tail[i:i+4],"little"):12d}')
