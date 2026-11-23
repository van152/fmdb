import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

arch='client'
raw=load(arch,7)
p,b,_,_=dp_walk(raw,f'{arch}7',14,len(raw)-8,208)
rows=[(x[0],x[1]) for x in b]

def items(q,lim,c):
    for _ in range(c):
        if q+12>lim: return None
        ln=struct.unpack_from('<I',raw,q+8)[0]
        if ln>4000 or q+12+ln>lim: return None
        q+=12+ln
    return q

pres=collections.Counter()
detail=[]
for i,(s,e) in enumerate(rows):
    nl=struct.unpack_from('<I',raw,s)[0]
    nm=raw[s+4:s+4+nl].decode('utf-8','replace')
    q0=s+4+nl
    sols=[]
    for u in range(q0, min(q0+16, e)):
        L=struct.unpack_from('<I',raw,u)[0]
        if L==0:
            pays=[b'']
        elif 4+L<=e-u:
            pl=raw[u+4:u+4+L]
            try: pays=[pl.decode('ascii')]
            except Exception: continue
            if ' ' in pays[0] or not pays[0]: continue
        else: continue
        mid=u+4+L
        for H in range(0,6):
            if mid+H+4>e-13: break
            c=struct.unpack_from('<I',raw,mid+H)[0]
            q2=items(mid+H+4,e-13,c)
            if q2 is not None and q2==e-13-5:
                sols.append((u-q0,H,c,L))
    pres[len(sols)]+=1
    if len(sols)==1:
        pre=raw[q0:sols[0][0]+0]
        detail.append((raw[q0:q0+sols[0][0]].hex(), sols[0]))
print('solution count dist:', dict(pres))
c2=collections.Counter((d[0], d[1][0], d[1][1], d[1][2]) for d in detail)
for k,v in c2.most_common(15): print(v,k)
print('prelen dist', collections.Counter(len(d[0])//2 for d in detail))
