import sys; sys.path.insert(0,'scripts')
import t74_frames_part2 as P
from t74_row_frames9 import payload, codec
import struct
c=codec(); b=payload(c,'client',21); r=P.fixed_rows(b,P.FIXED[('client',21)])
rows=r['rows']
for nm,off in (('Slat',17),('Slon',21)):
    f=[struct.unpack_from('<f',b,s+off)[0] for s,e in rows[:5000]]
    fin=[x for x in f if -180<=x<=180]
    print(nm,'f32 in [-180,180]:',len(fin),'/',len(f),'range',min(fin),max(fin))
print('row0 38B',b[14:52].hex(' '))
print('Scti@3',struct.unpack_from('<I',b,14+3)[0],'f32@17',struct.unpack_from('<f',b,14+17)[0],'f32@21',struct.unpack_from('<f',b,14+21)[0])
