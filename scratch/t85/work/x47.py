import json,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
for arch in ('client','server'):
    rows=[json.loads(l) for l in open(f'scratch/t50/out/profiles/table_{arch}_extra_9.rows.jsonl',encoding='utf-8')]
    pat=bytes.fromhex('ffffffffffffffff')
    okc=0; stridea=0; tail0=[]
    for r in rows:
        b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']; t=b[8+nl:]
        idx=[]; p=t.find(pat)
        while p>=0: idx.append(p); p=t.find(pat,p+1)
        if t[5]==len(idx): okc+=1
        if idx and set(idx[i+1]-idx[i] for i in range(len(idx)-1))=={27}: stridea+=1
        tail0.append(int.from_bytes(t[0:4],'little'))
    print(f'{arch}: count@tail+5 == #ff8 groups: {okc}/251 ; stride27 pure: {stridea}/251')
    print(f'   tail+0 u32: min={min(tail0)} max={max(tail0)} zero={sum(1 for x in tail0 if x==0)}')
