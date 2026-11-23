import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

def frames(arch,tid,n):
    raw=load(arch,tid)
    p,b,_,_ = dp_walk(raw,f'{arch}{tid}',14,len(raw)-8,n)
    assert b, (arch,tid,'no walk')
    return raw, [(s,e) for s,e,u in b], [u for _,_,u in b]

# t27: check middle constant
for arch in ('client','server'):
    raw,rows,uids = frames(arch,27,334)
    mids=[]
    for s,e in rows:
        nl=struct.unpack_from('<I',raw,s)[0]
        mids.append((s+4+nl, e-13))
    lens=[b-a for a,b in mids]
    print(arch,'t27 middle lens hist',collections.Counter(lens))
    print('  first row name',raw[rows[0][0]+4:rows[0][0]+4+struct.unpack_from('<I',raw,rows[0][0])[0]])
    print('  row lens min/max',min(e-s for s,e in rows),max(e-s for s,e in rows))
