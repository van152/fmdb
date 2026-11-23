import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

for arch in ('client','server'):
    raw=load(arch,7)
    p,b,_,_=dp_walk(raw,f'{arch}7',14,len(raw)-8,208)
    rows=[(x[0],x[1]) for x in b]
    print('===',arch)
    stat=collections.Counter()
    for i,(s,e) in enumerate(rows):
        nl=struct.unpack_from('<I',raw,s)[0]
        q=s+4+nl
        # url
        ul=struct.unpack_from('<I',raw,q+6)[0]
        ms=q+6+4+ul; me=e-13
        v=[struct.unpack_from('<I',raw,ms+22+4*k)[0] for k in range(3)]
        # find count position by parse
        found=None
        for H in (26,30):
            qq=ms+H
            if qq+4>me: continue
            c=struct.unpack_from('<I',raw,qq)[0]
            cur=qq+4; ok=True
            for _ in range(c):
                if cur+12>me: ok=False;break
                ln=struct.unpack_from('<I',raw,cur+8)[0]
                if ln>2000 or cur+12+ln>me: ok=False;break
                cur+=12+ln
            if ok and cur==me-5: found=(H,c); break
        stat[(found, v[0]==0xffffffff, v[1]<200, v[2] if v[2]<300 else 'big')]+=1
    for k,v in stat.most_common(10): print(v,k)
