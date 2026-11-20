import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections, bisect, hashlib, json

raw=load('server',24); n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
H=14; W=12; FOOT=9; F=n-FOOT
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
byo=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()): byo[o].append(p)
for k in byo: byo[k].sort()
cur=H; pos=[]
prev_uid=0; ok=True
for i in range(N):
    cs=byo[i]
    j=bisect.bisect_left(cs,cur)
    while j<len(cs) and struct.unpack_from('<I',raw,cs[j]+4)[0]<=prev_uid: j+=1
    if j>=len(cs) or cs[j]+W>F: ok=False; break
    p=cs[j]; pos.append(p); prev_uid=struct.unpack_from('<I',raw,p+4)[0]; cur=p+W
lens=[pos[0]+W-H]+[pos[i]-pos[i-1] for i in range(1,N)]
res=dict(payload=n,count=N,rows=len(pos),closure=(cur==F),walk_ok=ok,
  rowlen=[min(lens),max(lens)],rowlen_mean=round(sum(lens)/len(lens),3),
  sum_ok=(H+sum(lens)+FOOT==n), term_bytes=dict(collections.Counter(raw[p+W-1] for p in pos).most_common()),
  footer9=raw[n-FOOT:].hex(' '), footer8=raw[n-8:].hex(' '),
  ordinal_ok=all(struct.unpack_from('<I',raw,p)[0]==i for i,p in enumerate(pos)),
  uid_pair_ok=all(struct.unpack_from('<I',raw,p+4)[0]==struct.unpack_from('<I',raw,p+8)[0] for p in pos),
  uid_strict_incr=all(struct.unpack_from('<I',raw,pos[i]+4)[0]<struct.unpack_from('<I',raw,pos[i+1]+4)[0] for i in range(len(pos)-1)),
  sha=hashlib.sha256(raw).hexdigest(),
  hist={str(k):v for k,v in sorted(collections.Counter(lens).items())})
json.dump(res,open('scratch/t74/_stats_24b.json','w'),ensure_ascii=False)
print({k:v for k,v in res.items() if k!='hist'})
