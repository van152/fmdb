import json,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
pat=bytes.fromhex('ffffffffffffffff')
for arch in ('client','server'):
    rows=[json.loads(l) for l in open(f'scratch/t50/out/profiles/table_{arch}_extra_9.rows.jsonl',encoding='utf-8')]
    ok6=ok5=0; trail=collections.Counter(); starts=collections.Counter()
    for r in rows:
        b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']; t=b[8+nl:]
        idx=[];p=t.find(pat)
        while p>=0: idx.append(p); p=t.find(pat,p+1)
        if t[6]==len(idx): ok6+=1
        if t[5]==len(idx): ok5+=1
        if idx:
            s=idx[0]-19; starts[s]+=1
            trail[len(t)-s-27*len(idx)]+=1
    print(f'{arch}: count@tail+6==n_items {ok6}/251 ; count@tail+5 {ok5}/251')
    print('   item-start offsets:',dict(starts))
    print('   trailing bytes after last item:',dict(trail))
