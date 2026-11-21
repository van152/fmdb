import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
club=json.load(open('scratch/t88/club.json'))['uids']
cu=np.array(sorted(club),dtype=np.int64)
print('club n',len(cu),'min',cu.min(),'max',cu.max())
n=len(starts)
print('== u32 at row-start+o in club-UID set ==')
for o in range(0,72):
    v=np.array([struct.unpack_from('<I',b,s+o)[0] for s in starts])
    inn=np.isin(v,cu).mean()
    ff=(v==0xffffffff).mean()
    print(f'{o:3d} in_club={inn:6.3f} ff={ff:5.3f} med={int(np.median(v)):11d} uq={len(np.unique(v)):6d}')
