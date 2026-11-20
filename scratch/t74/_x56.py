import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections

raw=load('server',24)
n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
a=np.frombuffer(raw,dtype=np.uint8)
# unaligned u32 at every offset
w=np.lib.stride_tricks.sliding_window_view(a,4).view('<u4').ravel()[:n-3]
print('w len',len(w))
o=w[:len(w)-3]; u1=w[1:len(w)-2]; u2=w[2:len(w)-1]
mask=(u1==u2)&(u1>1000)&(u1<2**31)
pos=np.nonzero(mask)[0]
print('pair-equal positions (any align):',len(pos))
ords=o[mask]
sel=(ords<N)
print('with ord<N:',sel.sum())
p2=pos[sel]; o2=ords[sel]
print('sample',[(int(p),int(v)) for p,v in zip(p2[:10],o2[:10])])
print('last',[(int(p),int(v)) for p,v in zip(p2[-6:],o2[-6:])])
# check ordinal coverage
s=set(o2.tolist())
print('unique ords',len(s),'min',min(s),'max',max(s))
missing=[i for i in range(N) if i not in s]
print('missing count',len(missing),missing[:10])
