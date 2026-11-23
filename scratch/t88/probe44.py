import json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts)
b4=np.array([b[int(s)+4] for s in starts])
u,c=np.unique(b4,return_counts=True)
print('b4 full hist:'); print(dict(zip(u.tolist(),c.tolist())))
a0=np.array([int.from_bytes(b[int(s):int(s)+4],'little') for s in starts],dtype=np.int64)
key=list(zip(a0.tolist(),b4.tolist()))
print('distinct (a0,b4)',len(set(key)),'rows',n)
import collections
cc=collections.Counter(key)
print('dup multiplicity hist',{int(k):int(v) for k,v in zip(*np.unique(list(cc.values()),return_counts=True))})
