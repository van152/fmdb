import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct
raw=load('client',47)
for lo in (14,25):
    p,b,_,_=dp_walk(raw,f'c{lo}',lo,len(raw)-8,2488)
    print('lo',lo,'first3',[(x[0],x[1]) for x in b[:3]])
print('bytes 10..70:')
for j in range(10,72,16): print(f'  {j:3d} {raw[j:j+16].hex(" ")}')
print('identity@42..55', raw[42:55].hex(' '))
print('identity@47..60', raw[47:60].hex(' '))
