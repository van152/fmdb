import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends'])
club=set(json.load(open('scratch/t88/club.json'))['uids'])
n=len(starts); bb=np.frombuffer(b,np.uint8)
RT=[7,8,9,10,11,12,13,14,15,18,19,23,24,25,26,27,28]
print('membership of a0 sample in club:',100604 in club, 3044 in club)
print('== best byte columns by containment in RT ==')
res=[]
for o in range(0,67):
    col=bb[starts+o]
    f=float(np.isin(col,RT).mean()); u=len(np.unique(col))
    res.append((f,o,u))
res.sort(reverse=True)
for f,o,u in res[:12]: print(f'  +{o:3d} frac_rt={f:.4f} uniq={u}')
print('== u16 columns ==')
res=[]
for o in range(0,66):
    ok=np.ones(n,bool)
    col=np.array([struct.unpack_from('<H',b,s+o)[0] if s+o+2<=len(b) else 65535 for s in starts])
    res.append((float(np.isin(col,RT).mean()),o,len(np.unique(col)),int(col.max())))
res.sort(reverse=True)
for f,o,u,m in res[:12]: print(f'  +{o:3d} frac_rt={f:.4f} uniq={u} max={m}')
