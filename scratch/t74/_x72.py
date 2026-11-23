import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct
raw=load('server',24)
for p in (121,133,134,135,136):
    a,b,c=struct.unpack_from('<III',raw,p)
    print(p,'ord',a,'u1',b,'u2',c,'byte+12',raw[p+12])
print('raw 133..149', raw[133:149].hex(' '))
