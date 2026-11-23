import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, collections, bisect

raw=load('server',24); n=len(raw); N=struct.unpack_from('<I',raw,8)[0]
H=14; F=n-8; W=13
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
byo=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()): byo[o].append(p)
for k in byo: byo[k].sort()
cur=H; fpos=[]
for i in range(N):
    cs=byo[i]; j=bisect.bisect_left(cs,cur); p=cs[j]; fpos.append(p); cur=p+W
print('all 4-aligned?', all(p%4==0 for p in fpos), collections.Counter(p%4 for p in fpos))
b13=collections.Counter(raw[p+12] for p in fpos)
print('13th byte dist', b13.most_common(12), 'distinct', len(b13))
print('uid pairs equal all?', all(struct.unpack_from('<I',raw,p+4)[0]==struct.unpack_from('<I',raw,p+8)[0] for p in fpos))
print('ord==index all?', all(struct.unpack_from('<I',raw,p)[0]==i for i,p in enumerate(fpos)))
lens=[fpos[0]+W-H]+[fpos[i]-fpos[i-1] for i in range(1,N)]
print('rowlen 4-aligned-multiples?', collections.Counter((L-86)%4 for L in lens))
print('uid sample first5',[struct.unpack_from('<I',raw,p+4)[0] for p in fpos[:5]])
print('uid monotone?', None)
uids=[struct.unpack_from('<I',raw,p+4)[0] for p in fpos]
print('uid min/max',min(uids),max(uids),'strict incr?',all(uids[i]<uids[i+1] for i in range(len(uids)-1)))
np.save('scratch/t74/_fpos24.npy', np.array(fpos))
