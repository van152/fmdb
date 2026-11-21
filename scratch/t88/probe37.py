import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); RT=set(range(7,29))
ne=starts+41+sl
def col(width,o):
    out=np.empty(n,dtype=np.int64)
    for i in range(n):
        p=int(ne[i])+o
        if p+width>L: out[i]=-1; continue
        out[i]=int.from_bytes(b[p:p+width],'little')
    return out
print('== anchor=name_end (tail 0..25) ==')
for w in (1,2,4):
    for o in range(0,27-w+1):
        c=col(w,o)
        if c.min()<0: continue
        u=set(np.unique(c).tolist())
        if u<=RT and len(u)>1:
            print(f'  u{w*8} @ne+{o} vals={sorted(u)}')
        elif len(u)<=20 and max(u)<40:
            print(f'  cand u{w*8} @ne+{o} uniq={len(u)} {sorted(u)}')
