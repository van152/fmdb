import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); ne=starts+41+sl
club=np.array(sorted(json.load(open('scratch/t88/club.json'))['uids']),dtype=np.int64)
a0=np.array([int.from_bytes(b[int(s):int(s)+4],'little') for s in starts],dtype=np.int64)
# u32 columns anywhere in row (start+o) for o in 0..66 - fraction in club set
print('== u32 col membership: club / ff ==')
best=[]
for o in range(0,67-3):
    p=starts+o
    if p.max()+4>L: continue
    v=np.array([int.from_bytes(b[int(x):int(x)+4],'little') for x in p],dtype=np.int64)
    fc=float(np.isin(v,club).mean()); ff=float((v==0xffffffff).mean())
    best.append((max(fc,0),o,fc,ff,len(np.unique(v))))
best.sort(reverse=True)
for _,o,fc,ff,u in best[:14]:
    print(f'  +{o:3d} club={fc:.4f} ff={ff:.4f} uniq={u}')
print('\n== u32 col membership at name_end +o ==')
best=[]
for o in range(0,27-3):
    p=ne+o
    v=np.array([int.from_bytes(b[int(x):int(x)+4],'little') for x in p],dtype=np.int64)
    fc=float(np.isin(v,club).mean()); ff=float((v==0xffffffff).mean())
    best.append((fc,o,fc,ff,len(np.unique(v))))
best.sort(reverse=True)
for _,o,fc,ff,u in best[:14]:
    print(f'  ne+{o:3d} club={fc:.4f} ff={ff:.4f} uniq={u}')
