import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); ne=starts+41+sl
bb=np.frombuffer(b,np.uint8)
a0=np.array([struct.unpack_from('<I',b,s)[0] for s in starts])
u,c=np.unique(a0,return_counts=True)
print('groups',len(u),'rows/group: min',c.min(),'max',c.max(),'hist',{int(k):int(v) for k,v in zip(*np.unique(c,return_counts=True))})
# prefix byte columns with few distinct
print('\n== prefix byte columns (0..40) distinct<=16 ==')
for o in range(41):
    col=bb[starts+o]; uu,cc=np.unique(col,return_counts=True)
    if len(uu)<=16:
        print(f'{o:3d} uniq={len(uu):2d} {[(int(x),int(y)) for x,y in zip(uu,cc)]}')
print('\n== tail byte columns (rel name end, 0..25) distinct<=16 ==')
for k in range(26):
    col=bb[ne+k]; uu,cc=np.unique(col,return_counts=True)
    if len(uu)<=16:
        print(f'+{k:3d} uniq={len(uu):2d} {[(int(x),int(y)) for x,y in zip(uu,cc)]}')
