import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct
raw=load('client',7)
for s,e,i in [(14,204,0),(204,395,1),(395,632,2)]:
    b=raw[s:e]
    print('row',i,'len',len(b))
    print('  b[181:190]',b[181:190].hex() if len(b)>190 else None)
    print('  last 16', b[-16:].hex())
    for off in range(s,e-3):
        a,bb=struct.unpack_from('<II',raw,off)
        if a==bb and raw[off+8]==0:
            print('   match at rel',off-s,'val',a)
