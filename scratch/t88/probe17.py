import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
starts=np.array(json.load(open('scratch/t88/rows.json'))['starts'],dtype=np.int64)
ends=np.append(starts[1:],L-8)
# strlen @37
sl=np.frombuffer(b,'<u4',(L-37)//4,37)[ (starts-37)//4 ] if False else np.array([struct.unpack_from('<I',b,s+37)[0] for s in starts])
print('strlen stats min/max',sl.min(),sl.max(),'uniq',len(np.unique(sl)))
print('top',sorted(zip(*[x.tolist() for x in np.unique(sl,return_counts=True)]),reverse=True)[:6] if False else '')
u,c=np.unique(sl,return_counts=True); idx=np.argsort(-c)[:8]
print('strlen top:',[(int(u[i]),int(c[i])) for i in idx])
for i in (0,1,2,5,100):
    s,e=starts[i],ends[i]; L2=sl[i]
    name=b[s+41:s+41+L2]
    print(i,'len',e-s,'strlen',L2,repr(name), 'after', (s+41+L2))
json.dump({'starts':starts.tolist(),'ends':ends.tolist(),'strlen':sl.tolist()},open('scratch/t88/rows2.json','w'))
