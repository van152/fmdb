import json,sys
sys.stdout.reconfigure(encoding='utf-8')
for arch in ('client','server'):
    rows=[json.loads(l) for l in open(f'scratch/t50/out/profiles/table_{arch}_extra_9.rows.jsonl',encoding='utf-8')]
    print('==',arch,'min block len',min(r['len'] for r in rows))
    best=[]
    for off in range(0,220):
        ok=tot=0
        for r in rows:
            b=bytes.fromhex(r['raw_hex'])
            if off<len(b):
                tot+=1; ok+= (b[off]==(r['row']&0xff))
        best.append((ok,tot,off))
    best.sort(reverse=True)
    print(' top byte offsets by self-index hits:',best[:6])
    # u32 at 0xb9?
    for off in (0xb9,):
        ok=0
        for r in rows:
            b=bytes.fromhex(r['raw_hex'])
            if off+4<=len(b) and int.from_bytes(b[off:off+4],'little')==r['row']: ok+=1
        print(f'  u32 @ {off:#x} == row: {ok}/251')
