import numpy as np, collections
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
# keep only positions in increasing ordinal order check
order=np.argsort(P); P=P[order]; O=O[order]
first=collections.defaultdict(list)
for p,o in zip(P.tolist(),O.tolist()): first[o].append(p)
seq=[(o,first[o][0]) for o in range(84507) if o in first]
posv=[p for o,p in seq]
ordv=[o for o,p in seq]
diffs=np.diff(posv)
print('n rows found',len(seq),'monotone increasing?',bool((diffs>0).all()),'min diff',diffs.min() if len(diffs) else None)
print('dups among first-choice?', len(seq)-len(set(posv)))
print('gap stats: mean',diffs.mean(),'median',np.median(diffs),'max',diffs.max())
print('first 6',seq[:6]); print('last 3',seq[-3:])
# row length = next pos - pos; check identity at end: identity starts at pos, so row start = prevpos+12? 
# Instead: ordinal i's identity triple at pos_i => row i spans (prev_end, pos_i+13)
lens=[posv[i+1]-posv[i] for i in range(len(posv)-1)]
print('identity-start deltas: min',min(lens),'max',max(lens))
print('header to first identity',posv[0])
print('last identity to footer',len(open('scratch/t74/_p24.npy','rb'))*0, 8819030-posv[-1]-13)
