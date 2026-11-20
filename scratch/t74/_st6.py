import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections, hashlib, json

raw=load('server',24); n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
H=14; W=12; FOOT=9; F=n-FOOT
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
byo=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()): byo[o].append(p)
for k in byo: byo[k].sort()

# state: (endpos, uid) -> (count, parent_key)
states={(H,0):(1,None)}
layers={0:dict(states)}
for i in range(N):
    nxt={}
    for (q,pu),(c,_) in states.items():
        for p in byo[i]:
            if p<q: continue
            if p+W>F: break
            u=struct.unpack_from('<I',raw,p+4)[0]
            if u<=pu: continue
            key=(p+W,u)
            if key in nxt: nxt[key]=(nxt[key][0]+c,(q,pu))
            else: nxt[key]=(c,(q,pu))
    if not nxt: print('dead at layer',i,'states',len(states)); break
    states=nxt
    if len(states)<4000: layers[i+1]=dict(states)
print('layers stored',len(layers),'final states',len(states))
cands=[k for k in states if k[0]==F]
print('final at F:',[(k,states[k][0]) for k in cands])
