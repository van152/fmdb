import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

def rows_of(arch,tid,n):
    raw=load(arch,tid)
    _,b,_,_=dp_walk(raw,f'{arch}{tid}',14,len(raw)-8,n)
    return raw,[(x[0],x[1]) for x in b]

def tok_ok(raw,q,me):
    """one item: u32 a, u32 b, u32 len; if len==0xffffffff -> 12B else 12+len."""
    if q+12>me: return None
    a,b,ln=struct.unpack_from('<III',raw,q)
    if ln==0xffffffff: return q+12
    if ln>800: return None
    if q+12+ln>me: return None
    return q+12+ln

def fit(raw,ms,me):
    out=[]
    for H in range(0,42):
        if ms+H+4>me: break
        c=struct.unpack_from('<I',raw,ms+H)[0]
        if not (0<=c<400): continue
        q=ms+H+4; ok=True; spans=[]
        for _ in range(c):
            nq=tok_ok(raw,q,me)
            if nq is None: ok=False; break
            spans.append((q,nq)); q=nq
        if ok and q==me-5: out.append((H,c,spans))
    return out

for arch in ('client','server'):
    raw,rows=rows_of(arch,7,208)
    dist=collections.Counter(); Hs=collections.Counter(); fails=[]
    for i,(s,e) in enumerate(rows):
        nl=struct.unpack_from('<I',raw,s)[0]
        q0=s+4+nl+6
        L=struct.unpack_from('<I',raw,q0)[0]
        ms=q0+4+L; me=e-13
        f=fit(raw,ms,me)
        dist[len(f)]+=1
        if len(f)==1: Hs[(f[0][0],)]+=1
        else: fails.append((i,me-ms,f))
    print(arch,'fitcount',dict(dist),'H',dict(Hs))
    print('  fails',[(x[0],x[1],len(x[2])) for x in fails][:10])
