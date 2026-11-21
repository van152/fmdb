import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts)
def u32col(o,anchor='start'):
    base = starts if anchor=='start' else ends-13
    v=np.empty(n,dtype=np.uint64)
    for i in range(n):
        p=int(base[i])+o
        v[i]=int.from_bytes(b[p:p+4],'little') if p+4<=L else 0
    return v
def daterate(v):
    yr=(v>>16)&0xffff; mo=(v>>8)&0xff; dy=v&0xff
    ok=((yr>=1850)&(yr<=2120)&(mo>=1)&(mo<=12)&(dy>=1)&(dy<=31))
    return float(ok.mean()), float((v==0xffffffff).mean())
print('== u32 date4 scan (year<<16 | month<<8 | day) from row start ==')
for o in range(0,60):
    v=u32col(o)
    f,ff=daterate(v)
    if f>0.10: print(f'  +{o:3d} daterate={f:.4f} allff={ff:.3f}')
print('== from row end-13 (data region, offsets -13-4k) ==')
for o in range(-60,0):
    v=u32col(o,'end')
    f,ff=daterate(v)
    if f>0.10: print(f'  {o:3d} daterate={f:.4f} allff={ff:.3f}')
