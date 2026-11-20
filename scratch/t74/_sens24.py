import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections

raw=load('server',24); n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
H=14
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
byo=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()): byo[o].append(p)
for k in byo: byo[k].sort()

def paths(W,FOOT,pair):
    F=n-FOOT
    states={(H,0):1}
    for i in range(N):
        nxt={}
        for (q,pu),c in states.items():
            for p in byo[i]:
                if p<q: continue
                if p+W>F: break
                u=struct.unpack_from('<I',raw,p+4)[0]
                if pair:
                    if struct.unpack_from('<I',raw,p+8)[0]!=u: continue
                if u<=pu: continue
                key=(p+W,u); nxt[key]=nxt.get(key,0)+c
        if not nxt: return 0
        states=dict(sorted(nxt.items(),key=lambda kv:-kv[1])[:3000])
    return sum(c for k,c in states.items() if k[0]==F)

for W in (12,13,14):
    for FOOT in (7,8,9,10,12):
        print(f'W={W} footer={FOOT} pair+strictUID ->', paths(W,FOOT,True))
