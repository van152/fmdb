import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections

raw=load('server',24); n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
H=14; F=n-8; W=13
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
byo=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()): byo[o].append(p)
for k in byo: byo[k].sort()

# layer reachability forward
fwd=[set() for _ in range(N+1)]
fwd[0].add(H)
for i in range(N):
    cs=byo[i]
    for e in sorted(fwd[i]):
        for p in cs:
            if p<e: continue
            if p+W>F: break
            fwd[i+1].add(p+W)
    if not fwd[i+1]: print('dead',i); break
print('layer sizes', collections.Counter(len(s) for s in fwd))
# backward reachability
bwd=[set() for _ in range(N+1)]
bwd[N].add(F)
for i in range(N-1,-1,-1):
    cs=byo[i]
    for p in cs:
        if p+W>F: continue
        if p+W in bwd[i+1]:
            for e in fwd[i]:
                if e<=p: bwd[i].add(e)
print('bwd layer sizes', collections.Counter(len(s) for s in bwd))
print('live layers', sum(1 for i in range(N+1) if len(fwd[i]&bwd[i])))
amb=[i for i in range(N+1) if len(fwd[i]&bwd[i])>1]
print('ambiguous layers', len(amb), amb[:10])
