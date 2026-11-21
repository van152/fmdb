import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); RT=set(range(7,29))
def col(width,o,anchor):
    base = starts if anchor=='start' else ends-13
    out=np.empty(n,dtype=np.int64)
    for i in range(n):
        p=int(base[i])+o
        if p+width>L: out[i]=-1; continue
        out[i]=int.from_bytes(b[p:p+width],'little')
    return out
print('== anchor=row_start ==')
for w in (1,2,4):
    for o in range(0,67-w+1):
        c=col(w,o,'start')
        if c.min()>=0 and set(np.unique(c).tolist())<=RT:
            print(f'  u{w*8} @+{o} vals={sorted(set(c.tolist()))} counts={sorted(zip(*[x.tolist() for x in np.unique(c,return_counts=True)]))}')
