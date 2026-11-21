import json,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
for arch in ('client','server'):
    rows=[json.loads(l) for l in open(f'scratch/t50/out/profiles/table_{arch}_extra_9.rows.jsonl',encoding='utf-8')]
    pat=bytes.fromhex('ffffffffffffffff')
    cnt=collections.Counter(); stride_ok=0
    for r in rows:
        b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']
        tail=b[8+nl:]
        idx=[]; p=tail.find(pat)
        while p>=0: idx.append(p); p=tail.find(pat,p+1)
        d=[idx[i+1]-idx[i] for i in range(len(idx)-1)]
        if d and set(d)=={27}: stride_ok+=1
        cnt[len(idx)]+=1
    print('==',arch,'rows with pure 27-stride:',stride_ok,'/251')
    print('  #ff8 groups per row:',sorted(cnt.items()))
