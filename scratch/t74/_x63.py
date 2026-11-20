import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct, numpy as np, collections

raw=load('server',24)
n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
F=n-8
a=np.frombuffer(raw,dtype=np.uint8)
W=np.lib.stride_tricks.sliding_window_view(a,4).view('<u4').ravel()[:n-3]

def cands_in(lo,hi,i):
    out=[]
    for p in range(lo,min(hi,n-13)):
        if W[p]!=i: continue
        u1=W[p+1]; u2=W[p+2]
        out.append((p,u1,u2,a[p+12]))
    return out

print('ord0 window',cands_in(120,260,0)[:8])
print('ord1 window',cands_in(140,300,1)[:10])
print('ord2 window',cands_in(140,400,2)[:10])
print('ord10 near 75644',cands_in(75400,75800,10)[:6])
print('tail ord84505/84506',cands_in(8818700,8819022,84505), cands_in(8818700,8819022,84506))
