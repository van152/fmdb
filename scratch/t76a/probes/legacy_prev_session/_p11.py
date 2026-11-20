import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_c = core['load_payload']('client', 21)
H, n, Sc = 14, 48413, 38
mc = np.frombuffer(raw_c, np.uint8, H+n*Sc)[H:].reshape(n, Sc)
v7 = mc[:,7:11].copy().view('<u4').ravel()
nz = v7[v7 != 0xffffffff]
print('u32@7 non-ff count', len(nz), 'min', nz.min(), 'max', nz.max(), 'n<=250', int((nz<=250).sum()), 'n<48413', int((nz<48413).sum()), 'n(==0)', int((nz==0).sum()))
print('sample', nz[:20].tolist())
# byte0/1/2 vs others
for off in (0,1,11):
    u,c = np.unique(mc[:,off], return_counts=True)
    print('byte',off, dict(zip(u.tolist(), c.tolist())))
# cross tab byte0 x (u32@7 is ff)
isff = v7==0xffffffff
import collections
tab = collections.Counter(zip(mc[:,0].tolist(), isff.tolist()))
print('byte0 x u32@7sentinel', sorted(tab.items())[:24])
