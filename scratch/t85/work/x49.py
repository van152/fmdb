import json,sys
sys.stdout.reconfigure(encoding='utf-8')
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_client_extra_9.rows.jsonl',encoding='utf-8')]
pat=bytes.fromhex('ffffffffffffffff')
res=[]
for r in rows:
    b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']; t=b[8+nl:]
    idx=[];p=t.find(pat)
    while p>=0: idx.append(p); p=t.find(pat,p+1)
    if not idx: res.append((r['row'],len(t),None,None,None)); continue
    s=idx[0]-19
    cons=(len(t)-s)%27==0
    res.append((r['row'],len(t),s,len(idx),cons))
ok=sum(1 for x in res if x[4]); print('rows where (tail-s)%27==0:',ok,'/251')
bad=[x for x in res if x[2] is not None and not x[4]][:6]
print('examples failing:',bad)
print('no-ff8 rows:',sum(1 for x in res if x[2] is None))
for x in res[:8]: print(' row%-3d tail=%-4d itemstart=%-4s nff8=%-3s cons=%s'%x)
