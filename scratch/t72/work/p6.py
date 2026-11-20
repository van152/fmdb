import pickle, struct, numpy as np
from hashlib import sha256
from collections import Counter
raw=pickle.load(open('scratch/t72/work/raw.pkl','rb'))
U=lambda b,p=0: struct.unpack_from('<I',b,p)[0]
H=lambda x: sha256(x).hexdigest()

def identity_path(b, start, footer, width, lookahead, nonzero, increasing, team):
    n=U(b,8); end=len(b)-footer
    g=[[] for _ in range(n)]
    for shift in range(4):
        a=np.frombuffer(b,dtype='<u4',offset=shift,count=(len(b)-shift)//4)
        for x in np.flatnonzero((a[:-2]<n)&(a[1:-1]==a[2:])).tolist():
            at=4*x+shift; uid=int(a[x+1]); i=int(a[x])
            if at>=start and at+width<=end and (not nonzero or uid) and (lookahead is None or b[at+12] in lookahead):
                if team and (uid>U(b,len(b)-4) or (i<n-1 and b[at+12] not in (10,11))): continue
                if i!=n-1 or at+width==end: g[i].append((at,uid))
    links=[]; nexts=[]
    for i in range(n-1,-1,-1):
        d={}; here=[]
        for a,u in g[i]:
            if i==n-1: d[a]=None; here.append((a,u,1)); continue
            tot=0
            for z,v,c in nexts:
                if z>=a+width+team and (not increasing or u<v):
                    tot=min(2,tot+c); d[a]=z
                    if tot>=2: break
            if tot: here.append((a,u,tot))
        links.append(d); nexts=here
        if not nexts: return None
    if sum(c for _,_,c in nexts)!=1: return None
    a=nexts[0][0]; pts=[]
    for m in reversed(links):
        pts.append(a); a=m[a]
    return pts

b=raw['server',24]
pts=identity_path(b,14,9,12,None,True,False,True)
print('path?',pts is not None, len(pts) if pts else None)
if pts:
    first=13; ids={}; h=sha256(); sel=Counter()
    ok=True
    for i,at in enumerate(pts):
        x,u,v=struct.unpack_from('<III',b,at)
        if not (x==i and u==v): ok=False; print('bad',i,at,x,u,v); break
        ids[i]=u; sel[b[first]]+=1; h.update(struct.pack('<4I',i,first,at,u)); first=at+12
    print('ok',ok,'n',len(ids),'uniq',len(set(ids.values())),'first==',first,'len-9',len(b)-9)
    print('digest',h.hexdigest()[:20],'sel',dict(sel))
