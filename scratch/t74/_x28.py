import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

def rows_of(arch,tid,n,W=13,mk=True):
    raw=load(arch,tid)
    p,b,_,_ = dp_walk(raw,f'{arch}{tid}',14,len(raw)-8,n,W,mk)
    return raw, [(x[0],x[1]) for x in b]

raw,rows = rows_of('client',7,208)
M=[]
for s,e in rows:
    nl=struct.unpack_from('<I',raw,s)[0]
    p=s+4+nl+6
    ul=struct.unpack_from('<I',raw,p)[0]
    p+=4+ul
    M.append((p,e-13))

def items_ok(q,lim,c):
    while c>0:
        if q+12>lim: return None
        ln=struct.unpack_from('<I',raw,q+8)[0]
        if ln>600: return None
        q+=12+ln; c-=1
    return q

best=[]
for T in range(0,14):
  for H in range(0,44):
    hits=0
    for p,e in M:
        q=p+H
        if q+4>e: break
        c=struct.unpack_from('<I',raw,q)[0]
        if not (0<c<600): continue
        q2=items_ok(q+4,e,c)
        if q2 is None: continue
        if q2==e-T: hits+=1
    best.append((hits,T,H))
best.sort(reverse=True)
print('top',best[:8])
