import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
ne=starts+41+sl   # name end
bb=np.frombuffer(b,np.uint8)
print('== bytes relative to NAME END (tail, 26B) ==')
for k in range(0,27):
    col=bb[ne+k]; u,c=np.unique(col,return_counts=True)
    top=[(int(x),int(y)) for y,x in sorted(zip(c,u),reverse=True)[:4]]
    print(f'+{k:2d} uniq={len(u):3d} top={top}')
