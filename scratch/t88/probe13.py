import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
starts=np.array(json.load(open('scratch/t88/rows.json'))['starts'],dtype=np.int64)
ends=np.append(starts[1:],L-8)
rows=list(zip(starts.tolist(),ends.tolist()))
n=len(rows)
bb=np.frombuffer(b,np.uint8)
print('n',n)
# identity check at end-13
bad=0
for i,(s,e) in enumerate(rows):
    o,u1,u2=struct.unpack_from('<III',b,e-13)
    if o!=i or u1!=u2 or u1==0: bad+=1
print('bad_identity end-13',bad)
mk={}
for s,e in rows: mk[b[e-1]]=mk.get(b[e-1],0)+1
print('lastbyte',dict(sorted(mk.items(),key=lambda x:-x[1])[:6]))
# prefix profiling
print('\n--- prefix columns (row start +o) ---')
for o in range(0,72):
    vals=bb[starts+o]
    u,c=np.unique(vals,return_counts=True)
    top=sorted(zip(c.tolist(),u.tolist()),reverse=True)[:3]
    print(f'{o:3d} distinct={len(u):3d} top={[(v,k) for k,v in top]}')
