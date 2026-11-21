import json,struct
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); ne=starts+41+sl
refs=json.load(open('scratch/t88/refsets.json'))
S={k:np.array(sorted(v),dtype=np.int64) for k,v in refs.items()}
def col_u32(base,off):
    p=base+off
    return np.array([int.from_bytes(b[int(x):int(x)+4],'little') for x in p],dtype=np.int64)
print('slot            ff     zero   <2^31  club  comp  team  max')
rows=[]
for name,base,off in ([('S%d'%o,starts,o) for o in range(0,37,1)]+[('T%d'%k,ne,k) for k in (12,16,20)]):
    v=col_u32(base,off)
    ff=float((v==0xffffffff).mean())
    if ff>0.999 and len(np.unique(v))<=2: continue
    z=float((v==0).mean())
    rows.append((name,off,ff,z,float((v>0).mean()),float(np.isin(v,S['t3']).mean()),
                 float(np.isin(v,S['t25']).mean()),float(np.isin(v,S['t24']).mean()),int(v.max())))
for r in rows:
    print(f'{r[0]:6s} off={r[1]:3d} ff={r[2]:.3f} z={r[3]:.3f} club={r[5]:.3f} comp={r[6]:.3f} team={r[7]:.3f} max={r[8]}')
