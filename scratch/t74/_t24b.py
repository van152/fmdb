import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections

raw=load('server',24); n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
H=14; F=n-8
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
byo=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()): byo[o].append(p)
for k in byo: byo[k].sort()

def paths(W,footer,strict_uid):
    Fi=n-footer
    prev={H:1}
    for i in range(N):
        nxt={}
        for p in byo[i]:
            if p+W>Fi: break
            uid=struct.unpack_from('<I',raw,p+4)[0]
            s=0
            for q,c in prev.items():
                if q>p: continue
                if strict_uid:
                    pu=struct.unpack_from('<I',raw,q-4)[0] if q>H else 0
                    if uid<=pu: continue
                s+=c
            if s: nxt[p+W]=nxt.get(p+W,0)+s
        if not nxt: return 0
        prev={k:v for k,v in sorted(nxt.items())[:600]}
    return prev.get(Fi,0)

for W,fo in ((13,8),(12,9)):
    print(W,fo,'plain',paths(W,fo,False),'strict_uid',paths(W,fo,True))
    print('  strict, no-uid-eq: ', paths(W,fo,True))
