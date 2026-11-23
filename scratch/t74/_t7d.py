import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

for arch in ('client','server'):
    raw=load(arch,7)
    p,b,_,_=dp_walk(raw,f'{arch}7',14,len(raw)-8,208)
    rows=[(x[0],x[1]) for x in b]
    tails=collections.Counter(raw[e-18:e-13] for s,e in rows)
    print(arch,'DP paths',p,'rows',len(rows),'closure',rows[-1][1]==len(raw)-8)
    print('  pre-identity 5B:',tails.most_common(5),'distinct',len(tails))
    # interior length after url
    m=[]
    for i,(s,e) in enumerate(rows):
        nl=struct.unpack_from('<I',raw,s)[0]
        q=s+4+nl+6
        L=struct.unpack_from('<I',raw,q)[0]
        m.append(e-(q+4+L)-13)
    print('  midlen min/max',min(m),max(m),'len===mid+?', collections.Counter((e-s) for s,e in rows).most_common(3))
