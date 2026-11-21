import struct,json
from bisect import bisect_right
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b); n=84477
W=13
cand={}
for off in range(4):
    cnt=(L-off-3)//4
    w=np.frombuffer(b,'<u4',cnt,off)
    o,u1,u2=w[:cnt-2],w[1:cnt-1],w[2:cnt]
    mask=(o<n)&(u1>0)&(u1==u2)
    idx=np.nonzero(mask)[0]; pos=idx*4+off
    keep=(pos>=12)&(pos+W<=L-8)
    for p,oo,uu in zip(pos[keep].tolist(),o[idx][keep].tolist(),u1[idx][keep].tolist()):
        cand.setdefault(oo,[]).append((p,uu))
for k in cand: cand[k].sort()
def build(lo,hi):
    # state = end pos of row i ; value (count, prevEnd)
    cur={}
    for p,u in cand[0]:
        if p>=lo:  # row0 starts at lo, ends p+W ; require identity inside
            cur[p+W]=(1,(lo,u))
    if not cur: return None
    layers=[dict(cur)]
    for i in range(1,n):
        keys=sorted(cur); pref=[0]
        for k in keys: pref.append(pref[-1]+cur[k][0])
        def u_at(k): return cur[k][1][1]
        us=[u_at(k) for k in keys]
        nxt={}
        for p,u in cand[i]:
            e=p+W
            if e>hi: continue
            j=bisect_right(keys,p)  # prevEnd <= p
            # enforce uid increasing: find further restriction
            c=pref[j]
            if c<=0: continue
            nxt[e]=(c,keys[j-1])
        if not nxt: return ('dead',i)
        cur=nxt; layers.append(dict(cur))
    if hi not in cur: return ('nofin',hi)
    # reconstruct
    ends=[hi]; c=hi
    for i in range(n,0,-1):
        pe=layers[i][c][1]; ends.append(pe); c=pe
    ends.reverse()
    return ends
ends=build(14,L-8)
print(type(ends), ends if isinstance(ends,tuple) else (len(ends),ends[:4],ends[-1]))
