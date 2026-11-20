import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

raw=load('client',7)
p,b,_,_=dp_walk(raw,'c7',14,len(raw)-8,208)
rows=[(x[0],x[1]) for x in b]

def mid_of(s,e):
    nl=struct.unpack_from('<I',raw,s)[0]
    pp=s+4+nl+6
    ul=struct.unpack_from('<I',raw,pp)[0]
    return pp+4+ul, e-13, nl, ul

def items(q,lim,c):
    for _ in range(c):
        if q+12>lim: return None
        ln=struct.unpack_from('<I',raw,q+8)[0]
        if q+12+ln>lim: return None
        q+=12+ln
    return q

dist=collections.Counter(); bad=[]
for i,(s,e) in enumerate(rows):
    ms,me,nl,ul=mid_of(s,e)
    if me<ms: bad.append((i,'negmid',nl,ul,e-s)); continue
    fits=[]
    for H in range(20,44):
        if ms+H+4>me: break
        c=struct.unpack_from('<I',raw,ms+H)[0]
        if not (0<=c<400): continue
        q2=items(ms+H+4,me,c)
        if q2 is not None and q2==me-5: fits.append((H,c))
    dist[len(fits)]+=1
    if len(fits)!=1: bad.append((i,'fits',fits,e-s,nl,ul,me-ms))
print('rows with exactly 1 fit:',dist)
for x in bad[:12]: print(x)
