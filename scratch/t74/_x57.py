import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections

raw=load('server',24)
n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
a=np.frombuffer(raw,dtype=np.uint8)
allp=[]; allo=[]
for off in range(4):
    m=(n-off)//4
    w=np.frombuffer(raw,dtype='<u4',count=m,offset=off)
    o=w[:m-2]; u1=w[1:m-1]; u2=w[2:m]
    mask=(u1==u2)&(u1>1000)&(u1<2**31)&(o<N)
    idx=np.nonzero(mask)[0]
    if len(idx):
        allp.append(idx*4+off); allo.append(o[mask])
P=np.concatenate(allp); O=np.concatenate(allo)
order=np.argsort(P); P=P[order]; O=O[order]
print('total cands',len(P))
print('first 12',[(int(p),int(v)) for p,v in zip(P[:12],O[:12])])
s=set(O.tolist()); print('unique ords',len(s),'of',N,'missing',N-len(s))
cnt=collections.Counter(O.tolist())
print('dup dist',collections.Counter(cnt.values()))
np.save('scratch/t74/_p24.npy',P); np.save('scratch/t74/_o24.npy',O)
