import json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); ne=starts+41+sl
b4=np.array([b[int(s)+4] for s in starts])
def u32(base,off):
    return np.array([int.from_bytes(b[int(x)+off:int(x)+off+4],'little') for x in base],dtype=np.int64)
D=[u32(ne,o) for o in (0,4,8,12,16,20)]
print('rec_type  n    present(not-ff) fractions for tail u32 @ne+0,4,8,12,16,20')
for rt in sorted(set(b4.tolist())):
    m=b4==rt
    if m.sum()<20: continue
    fr=['%.2f'%float((D[j][m]!=0xffffffff).mean()) for j in range(6)]
    print(f'{rt:3d} {int(m.sum()):6d}  '+' '.join(fr))
