import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

raw=load('client',7)
p,b,_,_=dp_walk(raw,'c7',14,len(raw)-8,208)
rows=[(x[0],x[1]) for x in b]

def lstrs(s,e):
    out=[]
    for q in range(s,e-4):
        n=struct.unpack_from('<I',raw,q)[0]
        if n<3 or n>200 or q+4+n>e: continue
        seg=raw[q+4:q+4+n]
        try: t=seg.decode('utf-8')
        except Exception: continue
        if not t.isprintable(): continue
        # must be plain words / url chars
        if sum(ch.isalnum() for ch in t) < len(t)*0.7: continue
        out.append((q-s,q+4+n-s,n,t))
    return out

for i in (0,6,16,29):
    s,e=rows[i]
    print(f'=== row{i} len={e-s}')
    for o,no,n,t in lstrs(s,e):
        print(f'   lstr @+{o} n={n} end=+{no} {t[:50]!r}')
