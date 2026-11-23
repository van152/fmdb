import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

def rows_of(arch,tid,n):
    raw=load(arch,tid)
    p,b,_,_ = dp_walk(raw,f'{arch}{tid}',14,len(raw)-8,n)
    return raw, b

r1,rc = rows_of('client',18,1567)
r2,rs = rows_of('server',18,1567)
print('t18 client rows',len(rc),'server',len(rs))
for i in range(3):
    s,e,u=rc[i]; print('C row',i,e-s, r1[s:e][:70].hex(' '))
    s,e,u=rs[i]; print('S row',i,e-s, r2[s:e][:70].hex(' '))
print()
dc=[e-s for s,e,u in rc]; ds=[e-s for s,e,u in rs]
print('client lens min/max/mean',min(dc),max(dc),sum(dc)/len(dc))
print('server lens min/max/mean',min(ds),max(ds),sum(ds)/len(ds))
print('per-row diff hist', collections.Counter(a-b for a,b in zip(ds,dc)))
