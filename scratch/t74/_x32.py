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

def items(q,lim,c):
    for _ in range(c):
        if q+12>lim: return None
        ln=struct.unpack_from('<I',raw,q+8)[0]
        if ln>2000 or q+12+ln>lim: return None
        q+=12+ln
    return q

rule=collections.Counter(); bad=[]
for i,(s,e) in enumerate(rows):
    ms,me=mid_of(s,e)
    A=struct.unpack_from('<I',raw,ms+18)[0]
    if A==1:
        # expect extra u32 at 22, count at 30
        c=struct.unpack_from('<I',raw,ms+30)[0]
        q2=items(ms+34,me,c)
        ok = (q2==me-5)
        rule[('A1',ok,c if c<20 else 'big')]+=1
        if not ok: bad.append((i,'A1',me-ms,c,q2 if q2 is None else me-5-(q2)))
    else:
        c=struct.unpack_from('<I',raw,ms+26)[0]
        q2=items(ms+30,me,c)
        ok=(q2==me-5)
        rule[('A0',ok,A)]+=1
        if not ok: bad.append((i,'A0',me-ms,c,A))
print('rule matrix', dict(sorted(rule.items(), key=lambda x:-x[1])))
print('bad',len(bad),bad[:8])
# head 18 bytes: what is u32@4 and byte@5?
heads=collections.Counter()
for s,e in rows:
    ms,me=mid_of(s,e)
    heads[(struct.unpack_from('<I',raw,ms+4)[0], raw[ms+5], raw[ms+0])]+=1
print('head sig (u32@4, byte@5, byte@0):', heads.most_common(12))
