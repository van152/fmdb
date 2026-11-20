import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct, collections
for arch in ('client','server'):
    raw=load(arch,6); n=len(raw); c=struct.unpack_from('<I',raw,8)[0]
    H,F=14,8
    print(arch,'payload',n,'count',c,'closure16',H+c*16+F==n)
    # rdui@3 duni@7 within 16B row
    bad=0; okl=0; pat=collections.Counter()
    for i in range(c):
        p=H+i*16
        rdui,duni=struct.unpack_from('<II',raw,p+3)
        pat[(rdui,duni if duni<200 else 'big')]+=1
        if rdui==i: okl+=1
    print('  rdui==rowindex:',okl,'/',c)
    print('  first rows',[(struct.unpack_from('<II',raw,H+i*16+3)) for i in range(4)])
    for j in range(0,48,16): print(f'   {j:3d} {raw[H+j:H+j+16].hex(" ")}')
