import struct,sys
sys.path.insert(0,'scripts')
import numpy as np, t74_frames_part2 as P
for name,n in (('t25',7047),('t24',84507),('t45',84477)):
    b=open(f'scratch/t88/{name}.bin','rb').read(); L=len(b)
    cnt,st,_=P._dp(b,'x',14,L-8,n,13,strict_uid=True,pair=True)
    print(name,'paths',cnt,'first5',st[:5])
    for i in range(3):
        p=st[i]
        for d in (-13,0):
            q=p+d
            if q<0 or q+13>L: continue
            o,u1,u2,m=struct.unpack_from('<IIIB',b,q)
            print(f'  i={i} p={p} d={d} ord={o} u1={u1} u2={u2} mk={m}')
