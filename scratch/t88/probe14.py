import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
starts=np.array(json.load(open('scratch/t88/rows.json'))['starts'],dtype=np.int64)
n=len(starts)
def gather(base,width):
    if width==4:
        off=base%4
        v=np.frombuffer(b,'<u4',(L-off)//4,off)
        ix=base//4
        return v[ix]
    return np.frombuffer(b,'<u2',n,base) if base+2<=L else None
def stats(base,width,label,limit=1):
    pass
print('== u32 columns from row start ==')
for o in range(0,44):
    p=starts+o
    if p[-1]+4>L: print(o,'overflow'); break
    off=o%4
    v=np.frombuffer(b,'<u4',(L-off)//4,off)
    col=v[p//4]
    ff=(col==0xffffffff).mean(); lt=(col<84259).mean(); med=int(np.median(col))
    print(f'{o:3d} ff={ff:5.3f} lt84259={lt:5.3f} med={med:11d} max={int(col.max()):11d} uq={len(np.unique(col)):6d}')
