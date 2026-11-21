import json,collections
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); ne=starts+41+sl
b4=np.array([b[int(s)+4] for s in starts])
a0=np.array([int.from_bytes(b[int(s):int(s)+4],'little') for s in starts],dtype=np.int64)
print('b4 hist:',dict(sorted(collections.Counter(b4.tolist()).items())))
print('\nb4 -> n_clubs, rows/club max')
for k in sorted(set(b4.tolist())):
    m=b4==k
    print(f'  rt={k:3d} rows={int(m.sum()):6d} clubs={len(np.unique(a0[m])):5d}')
