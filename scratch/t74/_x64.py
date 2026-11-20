import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections

raw=load('server',24)
n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
ps=[];os_=[]
for off in range(4):
    m=(n-off)//4
    w=np.frombuffer(raw,dtype='<u4',count=m,offset=off)
    o=w[:m-2]; u1=w[1:m-1]; u2=w[2:m]
    mask=(u1==u2)&(u1>=1)&(u1<2**31)&(o<N)
    idx=np.nonzero(mask)[0]
    ps.append(idx*4+off); os_.append(o[mask])
P=np.concatenate(ps); O=np.concatenate(os_)
order=np.argsort(P); P=P[order]; O=O[order]
print('cands',len(P),'unique ords',len(set(O.tolist())),'of',N)
cnt=collections.Counter(O.tolist())
print('missing',N-len(cnt))
np.save('scratch/t74/_p24.npy',P); np.save('scratch/t74/_o24.npy',O)
# For low ordinals list all candidates
lo=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()):
    if o<12: lo[o].append(p)
for k in sorted(lo): print(k, lo[k][:5], len(lo[k]))
