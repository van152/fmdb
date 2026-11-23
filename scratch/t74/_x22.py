import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

def rows_of(arch,tid,n):
    raw=load(arch,tid)
    p,b,_,_ = dp_walk(raw,f'{arch}{tid}',14,len(raw)-8,n)
    return raw, [(x[0],x[1]) for x in b]

raw,rows = rows_of('client',18,1567)
print('t18 client mid contents:')
for i in range(0,10):
    s,e=rows[i]
    nl1=struct.unpack_from('<I',raw,s)[0]
    p=s+4+nl1
    nl2=struct.unpack_from('<I',raw,p)[0]
    p+=4+nl2
    mid=raw[p:e-13]
    print(f'row{i} len={e-s} nl=({nl1},{nl2}) midlen={len(mid)} mid={mid.hex(" ")}')
print()
mids=[]
for s,e in rows:
    nl1=struct.unpack_from('<I',raw,s)[0]
    p=s+4+nl1; nl2=struct.unpack_from('<I',raw,p)[0]; p+=4+nl2
    mids.append(len(e-13-p))
print('midlen hist', sorted(collections.Counter(mids).items()))
