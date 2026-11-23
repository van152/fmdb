import sys; sys.path.insert(0,'scripts')
import t74_frames_part2 as P
from t74_row_frames9 import payload, codec
import struct
c=codec()
for a,t,n in [('client',56,6),('client',0,3545),('client',8,126),('client',27,334),('client',7,208)]:
    b=payload(c,a,t)
    print(f'--- {a} {t} payload {len(b)}')
    for fo in (7,8,9,10,12):
        print(f'   footer{fo}:', b[len(b)-fo:].hex(' '))
