import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections, bisect

raw=load('server',24); n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
H=14; F=n-8
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
byo=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()): byo[o].append(p)
for k in byo: byo[k].sort()

W=13
# forward earliest: row i identity starts at p_i >= cur, cur=p_i+W
cur=H; fpos=[]
ok=True
for i in range(N):
    cs=byo[i]
    j=bisect.bisect_left(cs,cur)
    if j>=len(cs) or cs[j]+W>F: ok=False; break
    cur=cs[j]+W; fpos.append(cs[j])
print('forward ok',ok,'rows',len(fpos),'end',cur,'F',F,'match',cur==F)
if ok:
    lens=[fpos[0]+W-H]+[fpos[i]-fpos[i-1] for i in range(1,N)]
    print('rowlen min/median/max',min(lens),int(np.median(lens)),max(lens))
    print('len hist top', collections.Counter(lens).most_common(6))
    print('sum check',H+sum(lens)+8==n)
# backward latest: p_i <= lim, lim = p_{i-1}
lim=F; bpos=[None]*N; ok2=True
for i in range(N-1,-1,-1):
    cs=byo[i]
    j=bisect.bisect_right(cs,lim-W)
    if j==0: ok2=False; break
    p=cs[j-1]
    if i==0 and p<H: ok2=False;break
    bpos[i]=p; lim=p
print('backward ok',ok2,'start',lim,'H',H,'first',bpos[0])
if ok2 and ok:
    print('forward==backward?', fpos==bpos, 'diff count', sum(1 for a,b in zip(fpos,bpos) if a!=b))
