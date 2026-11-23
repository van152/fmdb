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
    return pp+4+ul, e-13

def parse(q,lim,c):
    for _ in range(c):
        if q+12>lim: return None
        ln=struct.unpack_from('<I',raw,q+8)[0]
        if ln>600: return None
        q+=12+ln
    return q

for i in range(12):
    s,e=rows[i]
    ms,me=mid_of(s,e)
    mid=raw[ms:me]
    cands=[]
    for H in range(0,min(48,len(mid))):
        if ms+H+4>me: break
        c=struct.unpack_from('<I',raw,ms+H)[0]
        if not (0<c<600): continue
        q2=parse(ms+H+4,me,c)
        if q2 is None: continue
        cands.append((H,me-q2,c))
    print(f'row{i} midlen={len(mid)} cands(H,tail,count)={cands}')
