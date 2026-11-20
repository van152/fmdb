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
cur=H; fpos=[]
for i in range(N):
    cs=byo[i]; j=bisect.bisect_left(cs,cur); p=cs[j]; fpos.append(p); cur=p+W
lens=[fpos[0]+W-H]+[fpos[i]-fpos[i-1] for i in range(1,N)]
mod=collections.Counter((L-86)%4 for L in lens)
print('mod4 of (len-86):',dict(mod))
print('dist',sorted(collections.Counter(lens).items())[:14])
print('total',sum(lens),'expected',F-H)
# which rows deviate from 86?
dev=[(i,L,fpos[i]) for i,L in enumerate(lens) if L!=86]
print('non-86 rows',len(dev), dev[:6])
