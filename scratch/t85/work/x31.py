import json,sys
sys.stdout.reconfigure(encoding='utf-8')
for arch in ('client','server'):
    rows=[json.loads(l) for l in open(f'scratch/t50/out/profiles/table_{arch}_extra_9.rows.jsonl',encoding='utf-8')]
    print('==',arch)
    # absolute byte 0xb9 from block start
    hits=[]
    for off in range(0,255):
        ok=0; tot=0
        for r in rows:
            b=bytes.fromhex(r['raw_hex'])
            if off<len(b):
                tot+=1
                if b[off]==(r['row']&0xff): ok+=1
        if tot>240 and ok>=tot-2: hits.append((off,ok,tot))
    print(' self-index byte offsets (>=tot-2):',hits)
    # name-relative
    hits2=[]
    for delta in range(0,200):
        ok=0; tot=0
        for r in rows:
            b=bytes.fromhex(r['raw_hex']); ne=8+r['marker']['name_len']
            off=ne+delta
            if off<len(b):
                tot+=1
                if b[off]==(r['row']&0xff): ok+=1
        if tot>240 and ok>=tot-2: hits2.append((delta,ok,tot))
    print(' self-index name-relative deltas:',hits2)
