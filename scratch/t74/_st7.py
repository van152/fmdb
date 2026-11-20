import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections, hashlib, json

raw=load('server',24); n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
H=14; W=12; FOOT=9; F=n-FOOT
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
byo=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()): byo[o].append(p)
for k in byo: byo[k].sort()

# exact reconstruction from the unique DP path
states={(H,0):(1,None)}
hist=[dict(states)]
for i in range(N):
    nxt={}
    for (q,pu),(c,_) in states.items():
        for p in byo[i]:
            if p<q: continue
            if p+W>F: break
            u=struct.unpack_from('<I',raw,p+4)[0]
            if u<=pu: continue
            key=(p+W,u)
            nxt[key]=(nxt.get(key,(0,None))[0]+c,(q,pu))
    states=nxt; hist.append(dict(states))
key=(F,None)
# choose the unique final
fin=[k for k in states if k[0]==F]
assert len(fin)==1, fin
cur=fin[0]; pos=[None]*N
for i in range(N,0,-1):
    q,pu=hist[i][cur][1]
    pos[i-1]=q   # start of row i-1 = prev end
    cur=(q,pu)
starts=pos
lens=[ (starts[i+1] if i+1<N else F) - starts[i] for i in range(N)]
# identity start for row i = end - W
idpos=[ (starts[i+1] if i+1<N else F) - W for i in range(N)]
res=dict(payload=n,count=N,rows=N,closure=True,
  header=H,footer=FOOT,identity_width=W,
  rowlen=[min(lens),max(lens)],rowlen_mean=round(sum(lens)/len(lens),3),
  sum_ok=(H+sum(lens)+FOOT==n),
  ordinal_ok=all(struct.unpack_from('<I',raw,idpos[i])[0]==i for i in range(N)),
  uid_pair_ok=all(struct.unpack_from('<I',raw,idpos[i]+4)[0]==struct.unpack_from('<I',raw,idpos[i]+8)[0] for i in range(N)),
  uid_strict_incr=all(struct.unpack_from('<I',raw,idpos[i]+4)[0]<struct.unpack_from('<I',raw,idpos[i+1]+4)[0] for i in range(N-1)),
  footer9=raw[F:].hex(' '), sha=hashlib.sha256(raw).hexdigest(),
  mod4=dict(collections.Counter(L%4 for L in lens)),
  hist={str(k):v for k,v in sorted(collections.Counter(lens).items())})
json.dump(res,open('scratch/t74/_stats_24b.json','w'),ensure_ascii=False)
print({k:v for k,v in res.items() if k!='hist'})
