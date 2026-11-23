import json,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
for arch in ('client','server'):
    rows=[json.loads(l) for l in open(f'scratch/t50/out/profiles/table_{arch}_extra_9.rows.jsonl',encoding='utf-8')]
    ok=0; fails=[]; hdr=collections.Counter(); tr=collections.Counter()
    for r in rows:
        b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']; t=b[8+nl:]
        n=t[6]; hdr[(t[4],t[5],t[7])]+=1
        end=8+27*n
        if end<=len(t) and len(t)-end==7: ok+=1
        else: fails.append((r['row'],len(t),n,len(t)-end))
    print(f'== {arch}: tail==8+27n+7 对 {ok}/251 ; fails {fails[:6]}')
    print('   header bytes (t[4],t[5],t[7]):',hdr.most_common(5))
