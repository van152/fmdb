import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
starts=np.array(json.load(open('scratch/t88/rows.json'))['starts'],dtype=np.int64)
ends=np.append(starts[1:],L-8)
lens=(ends-starts)
bb=np.frombuffer(b,np.uint8)
print('== columns relative to row END (k = bytes before end) ==')
for k in range(13,46):
    col=bb[ends-k]
    u,c=np.unique(col,return_counts=True)
    top=sorted(zip(c.tolist(),u.tolist()),reverse=True)[:3]
    print(f'-{k:3d} distinct={len(u):3d} top={[(v,hex(x)) for v,x in top]}')
