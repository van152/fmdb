import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts)
def vals(o,w=4):
    return np.array([int.from_bytes(b[int(s)+o:int(s)+o+w],'little') for s in starts],dtype=np.int64)
v=vals(34)
print('u32@34 uniq',len(np.unique(v)),'sample',np.unique(v)[:8].tolist())
print('  as u16 lo/hi:',np.unique(v&0xffff)[:8].tolist(),np.unique(v>>16)[:8].tolist())
# tail bytes at ne+0,2,4,6,8,10 look like [flag][..][7]
ne=starts+41+sl
for k in (0,2,4,6,8,10):
    c=np.array([int.from_bytes(b[int(ne[i])+k:int(ne[i])+k+1],'little') for i in range(n)])
    print(f'ne+{k} uniq={len(np.unique(c))} top',sorted(zip(*[x.tolist() for x in np.unique(c,return_counts=True)]),key=lambda t:-t[1])[:6])
