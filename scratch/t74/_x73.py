import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections, bisect

raw=load('server',24); n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
H=14; F=n-8; W=13
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
byo=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()): byo[o].append(p)
for k in byo: byo[k].sort()

# DP counting paths with parent tracking, enumerating all reaching states
states={H:1}          # endpos -> count
parents=[{} for _ in range(N+1)]   # parents[i][endpos] = list of (prev_end, cand_p)
parents[0]={H:None}
for i in range(N):
    cs=byo[i]; nxt={}; ks=sorted(states); run=0; jj=0
    for p in cs:
        if p+W>F: break
        while jj<len(ks) and ks[jj]<=p:
            run+=states[ks[jj]]; jj+=1
        if run:
            e=p+W
            nxt[e]=nxt.get(e,0)+run
    parents[i+1]=nxt
    states=nxt
    if not states: print('dead',i); break
print('paths final',states.get(F,0))
