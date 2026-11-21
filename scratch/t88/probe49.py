import json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); ne=starts+41+sl
def u(col,off,w=4):
    return np.array([int.from_bytes(b[int(x)+off:int(x)+off+w],'little') for x in col],dtype=np.int64)
def show(name,col,off,w=4):
    v=u(col,off,w)
    ff=float((v==(1<<(8*w))-1).mean()); z=float((v==0).mean())
    print(f'{name}+{off:3d} w{w} ff={ff:.3f} zero={z:.3f} uniq={len(np.unique(v))} min={v.min()} max={v.max()}')
print('--- TAIL 26 bytes (rel name end), u8 distinct ---')
for k in range(26):
    c=np.array([b[int(ne[i])+k] for i in range(n)])
    uu,cc=np.unique(c,return_counts=True)
    print(f'  k={k:2d} uniq={len(uu):3d} ff={float((c==255).mean()):.3f} top={[(int(a),int(y)) for a,y in sorted(zip(uu,cc),key=lambda t:-t[1])[:3]]}')
