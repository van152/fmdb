import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections, bisect, hashlib, json

raw=load('server',24); n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
H=14; F=n-8; W=13
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
byo=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()): byo[o].append(p)
for k in byo: byo[k].sort()
cur=H; fpos=[]
for i in range(N):
    cs=byo[i]; j=bisect.bisect_left(cs,cur); p=cs[j]; fpos.append(p); cur=p+W
lens=[fpos[0]+W-H]+[fpos[i]-fpos[i-1] for i in range(1,N)]
term=collections.Counter(raw[p+12] for p in fpos)
res=dict(payload=n,count=N,rows=len(fpos),closure=(cur==F),
  rowlen=[min(lens),max(lens)],rowlen_mean=round(sum(lens)/len(lens),3),
  mod4=dict(collections.Counter((L-86)%4 for L in lens)),
  terminator=dict(term.most_common()), first_anchor=fpos[0],
  hist={str(k):v for k,v in sorted(collections.Counter(lens).items())},
  sha=hashlib.sha256(raw).hexdigest(),
  ordinal_ok=all(struct.unpack_from('<I',raw,p)[0]==i for i,p in enumerate(fpos)),
  uid_pair_ok=all(struct.unpack_from('<I',raw,p+4)[0]==struct.unpack_from('<I',raw,p+8)[0] for p in fpos))
json.dump(res,open('scratch/t74/_stats_24.json','w'),ensure_ascii=False)
print({k:v for k,v in res.items() if k!='hist'})
