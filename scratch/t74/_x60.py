import numpy as np, collections, struct
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
s=set(O.tolist()); N=84507
missing=[i for i in range(N) if i not in s]
print('missing',len(missing))
# group into runs
runs=[]; st=missing[0]; pv=missing[0]
for m in missing[1:]:
    if m==pv+1: pv=m; continue
    runs.append((st,pv)); st=m; pv=m
runs.append((st,pv))
print('runs',len(runs),'largest',sorted(runs,key=lambda r:r[1]-r[0],reverse=True)[:8])
print('first 12 runs',runs[:12])
