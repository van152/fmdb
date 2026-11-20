import sys; sys.path.insert(0,'scripts')
from t74_row_frames9 import payload, codec, lstr, u32
import struct
c=codec(); b=payload(c,'client',8); F=len(b)-8
p=14; i=0
while i<4:
    q,n,t=lstr(b,p,F)
    suf=b[q:q+30]
    print(f'row{i} name={t!r} namelen={n} suffix_start={q}')
    print('   suffix hex', suf.hex(' '))
    print('   u32@suf+0 ',u32(b,q),' +4',u32(b,q+4),' +8',u32(b,q+8),' +12',u32(b,q+12),' +17',u32(b,q+17),' +21',u32(b,q+21))
    p=q+30; i+=1
