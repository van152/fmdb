import json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); ne=starts+41+sl
def vs(col):
    u,c=np.unique(col,return_counts=True)
    return {int(a):int(x) for a,x in zip(u,c)}
for o in (4,8,12,32):
    v=vs(np.array([b[int(s)+o] for s in starts]))
    print(f'b{o} n={len(v)} {dict(sorted(v.items())[:20])}')
print('u32@33',vs(np.array([int.from_bytes(b[int(s)+33:int(s)+37],'little') for s in starts])))
for k in (24,25):
    print(f'ne+{k}',vs(np.array([b[int(ne[i])+k] for i in range(n)])))
print('ne+13',vs(np.array([b[int(ne[i])+13] for i in range(n)])))
print('ne+14',vs(np.array([b[int(ne[i])+14] for i in range(n)])))
