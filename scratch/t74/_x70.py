import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections, bisect

raw=load('server',24); n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
byo=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()): byo[o].append(p)
for k in byo: byo[k].sort()

def grid(W, footer, marker):
    F=n-footer; H=14
    d=collections.defaultdict(list)
    for o in byo:
        for p in byo[o]:
            if marker and raw[p+W-1]!=0: continue
            d[o].append(p)
    if any(i not in d for i in range(N)): return ('missing',)
    prev={H:1}
    for i in range(N):
        nxt={}; ks=sorted(prev); run=0; jj=0
        for p in d.get(i,[]):
            if p+W>F: break
            while jj<len(ks) and ks[jj]<=p: run+=prev[ks[jj]]; jj+=1
            if run: nxt[p+W]=nxt.get(p+W,0)+run
        if not nxt: return ('dead',i)
        prev=nxt if len(nxt)<800 else dict(sorted(nxt.items())[:800])
    return prev.get(F,0)

for W in (12,13,14):
    for fo in (7,8,9,10,12):
        for mk in (False,True):
            print(f'W={W} footer={fo} marker={mk} ->', grid(W,fo,mk))
