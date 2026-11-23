import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct

raw=load('client',7)
def words(b):
    for i in range(0,len(b)-3,4):
        yield i, struct.unpack_from('<I',b,i)[0], b[i:i+4]

for s,e in [(14,204),(204,395),(395,632)]:
    b=raw[s:e]
    print(f'=== row {s} len {len(b)}')
    i=0
    while i < len(b):
        if i+4<=len(b):
            v=struct.unpack_from('<I',b,i)[0]
            # try string
            if v<300 and i+4+v<=len(b):
                cand=b[i+4:i+4+v]
                if all(32<=c<127 for c in cand) and v>2:
                    print(f'  {i:4d} STR len={v} {cand!r}')
                    i+=4+v
                    continue
            print(f'  {i:4d} u32 {v}  ({b[i:i+4].hex(" ")})')
        else:
            print(f'  {i:4d} tail {b[i:].hex()}')
        i+=4
    print()
