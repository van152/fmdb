import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

for arch in ('client','server'):
    raw=load(arch,7)
    p,b,_,_=dp_walk(raw,f'{arch}7',14,len(raw)-8,208)
    rows=[(x[0],x[1]) for x in b]
    print('===',arch,'first',rows[0],'last',rows[-1],'F',len(raw)-8)
    # identity window shift test: window of 13 bytes ending at e-d
    dist=collections.Counter()
    for i,(s,e) in enumerate(rows):
        good=[]
        for d in range(0,25):
            end=e-d
            if end-13<s: break
            o,u1,u2=struct.unpack_from('<III',raw,end-13)
            mk=raw[end-1]
            if o==i and u1==u2 and mk==0: good.append(d)
        dist[tuple(good)]+=1
    print(' identity end-shift candidates:', dist.most_common(5))
