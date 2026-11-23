import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections, bisect

raw=load('server',24); n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
H=14; F=n-8
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
byo=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()): byo[o].append(p)

for mk in (True,False):
    for k in byo: byo[k].sort()
    d=collections.defaultdict(list)
    for o in byo:
        for p in byo[o]:
            if (not mk) or raw[p+12]==0: d[o].append(p)
    sizes=collections.Counter(len(v) for v in d.values())
    print('marker',mk,'cand-size dist',dict(list(sizes.items())[:6]),'ords',len(d))
    # forward greedy
    cur=H; ok=True; fpos=[]
    for i in range(N):
        cs=d.get(i,[]); j=bisect.bisect_left(cs,cur)
        if j>=len(cs) or cs[j]+13>F: ok=False;break
        p=cs[j]; fpos.append(p); cur=p+13
    print('   greedy ok',ok,'end',cur,'==F',cur==F,'rows',len(fpos))
    if ok and cur==F:
        lens=[fpos[0]+13-H]+[fpos[i]-fpos[i-1] for i in range(1,N)]
        print('   len min/median/max',min(lens),int(np.median(lens)),max(lens),'sum',sum(lens)==F-H)
        print('   top',collections.Counter(lens).most_common(5))
        # path count
        prev={H:1}
        for i in range(N):
            nxt={}
            ks=sorted(prev)
            run=0; jj=0
            for p in d.get(i,[]):
                if p+13>F: break
                while jj<len(ks) and ks[jj]<=p: run+=prev[ks[jj]]; jj+=1
                if run: nxt[p+13]=nxt.get(p+13,0)+run
            if not nxt: print('   dead at',i); break
            prev=nxt if len(nxt)<800 else dict(sorted(nxt.items())[:800])
        print('   paths',prev.get(F,0))
