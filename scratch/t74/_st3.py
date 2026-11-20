import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections, hashlib, json

res={}
# ---- t7 media
for arch in ('client','server'):
    raw=load(arch,7); H,F=14,len(raw)-8
    p,b,_,_=dp_walk(raw,f'{arch}7',H,F,208)
    rows=[(x[0],x[1]) for x in b]
    lens=[e-s for s,e in rows]
    pre=collections.Counter(); url=0; midlens=[]
    for i,(s,e) in enumerate(rows):
        nl=struct.unpack_from('<I',raw,s)[0]; q=s+4+nl
        pre[raw[q:q+6].hex()]+=1
        L=struct.unpack_from('<I',raw,q+6)[0]
        if L: url+=1
        midlens.append(e-(q+6+4+L)-13)
    res[f'7_{arch}']=dict(payload=len(raw),rows=len(rows),closure=rows[-1][1]==F,
      lens=[min(lens),max(lens)],six=dict(pre.most_common(4)),six_distinct=len(pre),
      rows_with_url=url, mid=[min(midlens),max(midlens)],
      pre_ident=collections.Counter(raw[e-18:e-13].hex() for s,e in rows).most_common(3),
      sha=hashlib.sha256(raw).hexdigest())
# ---- t27
for arch in ('client','server'):
    raw=load(arch,27); H,F=14,len(raw)-8
    p=H;i=0;lens=[];bad=0;nl=[]
    while p<F:
        L=struct.unpack_from('<I',raw,p)[0]; e=p+4+L+95+13
        o,u1,u2=struct.unpack_from('<III',raw,e-13)
        if not(o==i and u1==u2 and raw[e-1]==0): bad+=1
        lens.append(e-p); nl.append(L); p=e; i+=1
    res[f'27_{arch}']=dict(payload=len(raw),rows=i,closure=(p==F),bad=bad,
      lens=[min(lens),max(lens)],namelen=[min(nl),max(nl)],
      sha=hashlib.sha256(raw).hexdigest(),
      hist={str(k):v for k,v in sorted(collections.Counter(lens).items())})
# ---- t24 footer / tail
raw=load('server',24)
res['24_tail']=dict(payload=len(raw),last16=raw[-16:].hex(' '),footer8=raw[len(raw)-8:].hex(' '),
   head16=raw[:16].hex(' '), count=struct.unpack_from('<I',raw,8)[0])
print(json.dumps(res,ensure_ascii=False,indent=1)[:3000])
open('scratch/t74/_stats_b.json','w').write(json.dumps(res,ensure_ascii=False))
