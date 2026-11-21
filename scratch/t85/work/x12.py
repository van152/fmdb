import json,sys,struct
sys.stdout.reconfigure(encoding='utf-8')
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_client_extra_9.rows.jsonl',encoding='utf-8')]
print('rows',len(rows))
bad={}
for off in range(0,200):
    ok=sum(1 for r in rows if off<r['len'] and int(r['raw_hex'][2*off:2*off+2] or 'ff',16)==(r['row']&0xff))
    if ok>=250: print('byte offset',off,'self-index matches',ok,'/251')
# also u32 self index
for off in range(0,180):
    ok=0
    for r in rows:
        h=r['raw_hex']
        if 2*(off+4)<=len(h) and struct.unpack('<I',bytes.fromhex(h[2*off:2*off+8]))[0]==r['row']: ok+=1
    if ok>=250: print('u32 offset',off,'self-index matches',ok)
