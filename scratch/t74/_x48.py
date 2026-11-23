import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections

raw=load('server',24)
a=np.frombuffer(raw,dtype=np.uint8)
n=len(a)
print('payload',n,'len%4',n%4)
H=14
print('head',raw[:48].hex(' '))
print('u32@8',struct.unpack_from('<I',raw,8)[0])
print('tail 16',raw[-16:].hex(' '))

# vectorized: all positions p (any alignment) with u32@p == u32@p+4, marker p+12==0
b=np.frombuffer(raw,dtype='<u4',count=(n-16)//4,offset=0)
# aligned only first
o=b[0:len(b)-3]
u1=b[1:len(b)-2]
u2=b[2:len(b)-1]
m=a[12::4][:len(o)]
mask=(u1==u2)&(u1>0)&(u1<200000)&(m==0)
idx=np.nonzero(mask)[0]*4
print('aligned identity-like count',len(idx))
print('first 20 (pos,ord,uid)',[(int(p),int(struct.unpack_from('<I',raw,p)[0]),int(struct.unpack_from('<I',raw,p+4)[0])) for p in idx[:20]])
ords=np.array([struct.unpack_from('<I',raw,int(p))[0] for p in idx[:5000]])
print('first 30 ords',ords[:30])
print('ord min/max within first 5000',ords.min(),ords.max(),'unique',len(set(ords.tolist())))
