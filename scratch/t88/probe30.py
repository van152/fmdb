import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends'])
n=len(starts)
ordv=np.array([struct.unpack_from('<I',b,e-13)[0] for e in ends])
u1=np.array([struct.unpack_from('<I',b,e-9)[0] for e in ends])
u2=np.array([struct.unpack_from('<I',b,e-5)[0] for e in ends])
idx=np.arange(n)
print('ord==idx',bool((ordv==idx).all()))
print('u1==u2',bool((u1==u2).all()))
print('u1==ord+1',bool((u1==ordv+1).all()), 'diff hist',{int(k):int(v) for k,v in zip(*np.unique(u1-ordv,return_counts=True))})
print('marker set',set(b[e-1] for e in ends))
