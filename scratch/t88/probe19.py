import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts)
print('rowlen==80+strlen all?',bool((ends-starts==80+sl).all()))
a0=np.array([struct.unpack_from('<I',b,s)[0] for s in starts])
u,c=np.unique(a0,return_counts=True)
print('u32@0: uniq',len(u),'min',u.min(),'max',u.max())
print('count hist of multiplicity',{int(k):int(v) for k,v in zip(*np.unique(c,return_counts=True))})
print('top dup values',[(int(u[i]),int(c[i])) for i in np.argsort(-c)[:5]])
print('max value rows',int(u[-1]))
# u8 @ 4..12
bb=np.frombuffer(b,np.uint8)
for o in range(0,14):
    col=bb[starts+o]; uu,cc=np.unique(col,return_counts=True)
    print(f'byte {o:2d} uniq={len(uu):3d} top={[(int(x),int(y)) for y,x in sorted(zip(cc,uu),reverse=True)[:3]]}')
