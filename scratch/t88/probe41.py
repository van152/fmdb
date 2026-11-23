import struct,json
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b)
d=json.load(open('scratch/t88/rows2.json')); starts=np.array(d['starts']); ends=np.array(d['ends']); sl=np.array(d['strlen'])
n=len(starts); bb=np.frombuffer(b,np.uint8)
ne=starts+41+sl
a0=np.array([int.from_bytes(b[int(s):int(s)+4],'little') for s in starts],dtype=np.int64)
club=set(json.load(open('scratch/t88/club.json'))['uids'])
# comp uids from t25
c25=open('scratch/t88/t25.bin','rb').read()
import sys; sys.path.insert(0,'scripts')
import t74_frames_part2 as P
cnt,cs,_=P._dp(c25,'t25',14,len(c25)-8,7047,13,strict_uid=True,pair=True)
compu=set()
for p in cs:
    e=p+13; compu.add(struct.unpack_from('<I',c25,e-9)[0])
print('comp rows',len(compu))
bad=a0[~np.isin(a0,list(club))]
print('not-club rows',len(bad),'distinct',len(np.unique(bad)))
print('in comp',int(np.isin(np.unique(bad),list(compu)).sum()),'of',len(np.unique(bad)))
print('range',bad.min(),bad.max())
print('frac <57',float((bad<57).mean()))
print('sample',sorted(np.unique(bad))[:20])
# rec_type search: exact subset of RT set
RT={7,8,9,10,11,12,13,14,15,18,19,23,24,25,26,27,28}
print('\n== columns whose value set == RT exactly ==')
for anchor,name in ((starts,'start'),(ne,'ne')):
    for o in range(0,30 if name=='ne' else 40):
        col=np.array([int(b[int(p)+o]) for p in anchor])
        u=set(np.unique(col).tolist())
        if u<=RT and len(u)>=8: print(f'  {name}+{o} uniq={len(u)} {sorted(u)}')
