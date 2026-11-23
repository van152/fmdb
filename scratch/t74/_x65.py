import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections

raw=load('server',24); n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
byo=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()): byo[o].append(p)
H=14; F=n-8
# chain DP with constraints: row i end = p_i+13, p strictly increasing, 13<=gap<=400
cand=[[p for p in sorted(byo[i]) if H<=p and p+13<=F] for i in range(N)]
print('cand sizes', collections.Counter(len(c) for c in cand))
reach={H: True}   # position where row i starts (prev end)
import array
front={H:None}
est=array.array('i',[-1])*(0)
# forward: for each i, compute reachable positions (row start)
cur={H}
lens=[]
for i in range(N):
    nxt=set(); mp={}
    cs=cand[i]
    for p in cs:
        for st in cur:
            if st<=p and 13<=p+13-st<=400:
                nxt.add(p+13); mp[p+13]=st; break
    cur=nxt
    if not cur: print('dead at',i,'cand',len(cs)); break
    if len(cur)>50: cur=set(sorted(cur)[:50])
print('rows processed',i+1,'final reachable',sorted(cur)[:5],'F',F,'hit',F in cur)
