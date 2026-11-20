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
# DP path counting: layer i positions set with counts (paths), require p_i >= prev+W
prev={H:1}
for i in range(N):
    cs=byo[i]; nxt={}
    for p in cs:
        if p+W>F: break
        # sum counts of prev positions <= p
        s=0
        for q,c in prev.items():
            if q<=p: s+=c
        if s: nxt[p+W]=nxt.get(p+W,0)+s
    if not nxt: print('dead',i); break
    prev={k:v for k,v in sorted(nxt.items())[:400]}
print('paths to F at N rows:', prev.get(F,0))
