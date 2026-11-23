import json,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_client_extra_9.rows.jsonl',encoding='utf-8')]
b=bytes.fromhex(rows[0]['raw_hex']); nl=rows[0]['marker']['name_len']
tail=bytes(b[8+nl:])
print('tail',len(tail))
# find offsets of "ff ff ff ff ff ff ff ff 00 00 00"
pat=bytes.fromhex('ffffffffffffffff')
idx=[]; p=tail.find(pat)
while p>=0: idx.append(p); p=tail.find(pat,p+1)
print('ff*8 at',idx)
print('deltas',[idx[i+1]-idx[i] for i in range(len(idx)-1)])
# find the u32 counters
for i in range(len(tail)-3):
    pass
