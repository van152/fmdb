import struct, json
from bisect import bisect_right
import numpy as np
b=open('scratch/t88/t45.bin','rb').read(); L=len(b); n=84477
def scan(nmax,W=13):
    cand={}
    for off in range(4):
        cnt=(L-off-3)//4
        w=np.frombuffer(b,'<u4',cnt,off)
        if cnt<3: continue
        o,u1,u2=w[:cnt-2],w[1:cnt-1],w[2:cnt]
        mask=(o<nmax)&(u1>0)&(u1==u2)
        idx=np.nonzero(mask)[0]
        pos=idx*4+off
        for p,oo,uu in zip(pos.tolist(),o[idx].tolist(),u1[idx].tolist()):
            cand.setdefault(oo,[]).append((p,uu))
    for k in cand: cand[k].sort()
    return cand
def dp(cand,H,F,W=13,cap=10**9):
    hi=L-F
    if any(i not in cand for i in range(n)): return 0,None
    prev={p:1 for p,u in cand[0] if p>=H-W and p+W<=hi}
    back=[dict((p,None) for p in prev)]
    for i in range(1,n):
        keys=sorted(prev); pref=[0]
        for k in keys: pref.append(pref[-1]+prev[k])
        cur={}
        for p,u in cand[i]:
            if p+W>hi: continue
            j=bisect_right(keys,p-W)
            if j==0: continue
            c=min(cap,pref[j])
            if c: cur[p]=c
        if not cur: return 0,None
        back.append(dict((p,q) for p in cur for q in [0])) # placeholder
        prev=cur
    fin=[p for p in prev if p+W==hi]
    if not fin: return 0,None
    total=min(cap,sum(prev[p] for p in fin))
    return total, None
def dp_trace(cand,H,F,W=13):
    hi=L-F
    prev={p:1 for p,u in cand[0] if p>=H-W and p+W<=hi}
    layers=[dict(prev)]
    for i in range(1,n):
        keys=sorted(prev); pref=[0]
        for k in keys: pref.append(pref[-1]+prev[k])
        cur={}
        for p,u in cand[i]:
            if p+W>hi: continue
            j=bisect_right(keys,p-W)
            if j==0: continue
            c=pref[j]
            if c: cur[p]=(c,keys[j-1])
        if not cur: return None,None
        layers.append(dict(cur)); prev={k:v[0] for k,v in cur.items()}
    fin=[p for p in prev if p+W==hi]
    if len(fin)!=1 or prev[fin[0]]!=1: return None,None
    pos=fin[0]; ids=[pos]
    for i in range(n-1,0,-1):
        pos=layers[i][pos][1]; ids.append(pos)
    ids.reverse()
    return ids,layers
cand=scan(n)
print({k:len(v) for k,v in list(cand.items())[:3]}, 'ordinals',len(cand))
for H,F in ((12,8),(14,8)):
    tot,_=dp(cand,H,F)
    print('H',H,'F',F,'paths',tot)
ids,_=dp_trace(cand,14,8)
if ids:
    bounds=[14]+[p+13 for p in ids]
    rows=[(bounds[i],bounds[i+1]) for i in range(n)]
    print('closure',bounds[-1],L-8, bounds[-1]==L-8)
    lens=[e-s for s,e in rows]; print('lens',min(lens),max(lens),len(set(lens)),sum(lens))
    # identity check
    bad=0; mk={}
    for i,(s,e) in enumerate(rows):
        o,u1,u2=struct.unpack_from('<III',b,e-13)
        if o!=i or u1!=u2 or u1==0: bad+=1
        mk[b[e-1]]=mk.get(b[e-1],0)+1
    print('bad_identity',bad,'lastbyte',mk)
    print('first5',rows[:5])
    print('row0',b[14:rows[0][1]].hex(' '))
