import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections

raw=load('server',24)
n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
print('payload',n,'count',N)
a=np.frombuffer(raw,dtype=np.uint8)
w=np.frombuffer(raw,dtype='<u4',count=(n//4),offset=0)  # aligned words only
M=len(w)
o=w[:M-2]; u1=w[1:M-1]; u2=w[2:M]
mask=(u1==u2)&(u1>0)&(u1<2**24)&(o<N)
pos=(np.nonzero(mask)[0]*4)
ordv=o[mask]
print('aligned cand positions (pair, ord<N):',len(pos))
mk=np.array([a[p+12] for p in pos])
print('marker0 share',(mk==0).mean())
# distribution of ordinals
cnt=collections.Counter(ordv.tolist())
print('ordinal dup dist', collections.Counter(cnt.values()))
missing=[i for i in range(N) if i not in cnt]
print('missing ordinals',len(missing),missing[:10])
