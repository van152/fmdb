import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

for arch in ('client','server'):
    raw=load(arch,27)
    p,b,_,_=dp_walk(raw,f'{arch}27',14,len(raw)-8,334)
    rows=[(x[0],x[1]) for x in b]
    mid=collections.Counter(); bad=[]
    for i,(s,e) in enumerate(rows):
        L=struct.unpack_from('<I',raw,s)[0]
        nl = L if L<4096 and s+4+L<=e else None
        # try both offset 0 and 2
        for off in (0,2):
            if s+off+4<=e:
                ln=struct.unpack_from('<I',raw,s+off)[0]
                if ln<4096 and s+off+4+ln<=e:
                    if e-(s+off+4+ln+13)==95: mid[(off,'95')]+=1; break
        else: bad.append((i,e-s))
    print(arch,'midlen fit',dict(mid),'bad',len(bad),bad[:6])
