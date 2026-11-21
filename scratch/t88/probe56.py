import struct,sys
sys.path.insert(0,'scripts')
import numpy as np, t74_frames_part2 as P
for name,n in (('t25',7047),('t24',84507)):
    b=open(f'scratch/t88/{name}.bin','rb').read(); L=len(b)
    for W,F in ((13,8),(12,8),(13,9),(14,8)):
        cnt,st,_=P._dp(b,'x',14,L-F,n,W,strict_uid=True,pair=True)
        print(name,'W',W,'F',F,'paths',cnt)
    cnt,st,_=P._dp(b,'x',14,L-8,n,13,strict_uid=True,pair=True)
    if st:
        ends=[p+W for p in st][:5]
        for i,p in enumerate(st[:5]):
            print('  i',i,'p',p,'ord',struct.unpack_from('<I',b,p)[0])
