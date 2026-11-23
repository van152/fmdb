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
    if not (0<c<600): return None
    for _ in range(c):
        if q+12>lim: return None
        ln=struct.unpack_from('<I',raw,q+8)[0]
        if ln>800: return None
        q+=12+ln
    return q

stats=collections.Counter()
for i,(s,e) in enumerate(rows):
    ms,me=mid_of(s,e)
    opt=[]
    for H in (26,30):
        if ms+H+4>me: continue
        c=struct.unpack_from('<I',raw,ms+H)[0]
        q2=parse(ms+H+4,me,c)
        if q2 is not None and q2==me-5:
            opt.append((H,c))
    u18=struct.unpack_from('<I',raw,ms+18)[0] if ms+22<=me else None
    u26=struct.unpack_from('<I',raw,ms+26)[0] if ms+30<=me else None
    stats[(tuple(opt), u18, u26)]+=1
for k,v in sorted(stats.items(), key=lambda x:-x[1]):
    print(v, k)
