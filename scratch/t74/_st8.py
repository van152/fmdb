import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections, hashlib, json

raw=load('server',24); n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
H=14; W=13; FOOT=8; F=n-FOOT
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
byo=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()): byo[o].append(p)
for k in byo: byo[k].sort()

states={(H,0):(1,None)}; hist=[dict(states)]
for i in range(N):
    nxt={}
    for (q,pu),(c,_) in states.items():
        for p in byo[i]:
            if p<q: continue
            if p+W>F: break
            u=struct.unpack_from('<I',raw,p+4)[0]
            if struct.unpack_from('<I',raw,p+8)[0]!=u: continue
            if u<=pu: continue
            key=(p+W,u); nxt[key]=(nxt.get(key,(0,None))[0]+c,(q,pu))
    states=nxt; hist.append(dict(states))
fin=[k for k in states if k[0]==F]
print('finals',len(fin))
cur=fin[0]; starts=[None]*N
for i in range(N,0,-1):
    q,pu=hist[i][cur][1]; starts[i-1]=q; cur=(q,pu)
lens=[(starts[i+1] if i+1<N else F)-starts[i] for i in range(N)]
idp=[(starts[i+1] if i+1<N else F)-W for i in range(N)]
sel=collections.Counter(raw[p+12] for p in idp)
res=dict(payload=n,count=N,rows=N,closure=(H+sum(lens)+FOOT==n),
  header=H,footer=FOOT,identity_width=13,
  identity_layout="ordinal@+0 UID@+4 UID@+8 selector@+12",
  selector_dist=dict(sel.most_common()),
  rowlen=[min(lens),max(lens)],rowlen_mean=round(sum(lens)/len(lens),3),
  ordinal_ok=all(struct.unpack_from('<I',raw,idp[i])[0]==i for i in range(N)),
  uid_pair_ok=all(struct.unpack_from('<I',raw,idp[i]+4)[0]==struct.unpack_from('<I',raw,idp[i]+8)[0] for i in range(N)),
  uid_strict_incr=all(struct.unpack_from('<I',raw,idp[i]+4)[0]<struct.unpack_from('<I',raw,idp[i+1]+4)[0] for i in range(N-1)),
  footer8=raw[F:].hex(' '), sha=hashlib.sha256(raw).hexdigest(),
  hist={str(k):v for k,v in sorted(collections.Counter(lens).items())})
json.dump(res,open('scratch/t74/_stats_24c.json','w'),ensure_ascii=False)
print({k:v for k,v in res.items() if k!='hist'})
print('n distinct rowlens',len(res['hist']))
