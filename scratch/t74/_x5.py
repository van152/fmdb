import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct
for arch,tid,rows in [('client',7,[(14,204),(204,395),(395,632)]),
                      ('client',18,[(14,99),(99,182),(182,269)])]:
    raw=load(arch,tid)
    print('===',arch,tid,len(raw))
    for i,(s,e) in enumerate(rows):
        b=raw[s:e]
        print(f' row{i} len={len(b)} last14={b[-14:].hex(" ")}  u32s_last={(struct.unpack_from("<III",b,len(b)-13), b[-1])}')
