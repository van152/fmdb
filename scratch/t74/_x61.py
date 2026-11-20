import numpy as np, collections
P=np.load('scratch/t74/_p24.npy'); O=np.load('scratch/t74/_o24.npy')
first={}
for p,o in zip(P.tolist(),O.tolist()):
    if o not in first: first[o]=p
ords=sorted(first)
sub=[o for o in ords if o>=863]
pos=[first[o] for o in sub]
d=np.diff(pos)
print('rows>=863:',len(sub),'monotone',bool((d>0).all()))
bad=np.nonzero(d<0)[0]
print('violations',len(bad))
if len(bad): print('first viol at ord',sub[bad[0]],sub[bad[0]+1],pos[bad[0]],pos[bad[0]+1])
print('gap stats mean',d.mean(),'median',np.median(d),'min',d.min(),'max',d.max())
print('first 8 [(o,pos)]',[(sub[i],pos[i]) for i in range(8)])
# check ord vs index sequentiality: does sub == range? 
print('sub is contiguous from 863 to 84506?', sub[0], sub[-1], len(sub), 84507-863)
missing=[o for o in range(863,84507) if o not in first]
print('missing in tail',len(missing),missing[:5])
