import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n, Ss = 14, 48413, 181
ms = np.frombuffer(raw_s, np.uint8, H+n*Ss)[H:].reshape(n, Ss)
pre = ms[:, 0:143]
nz = (pre != 0).sum(axis=1)
order = np.argsort(nz)
print('nonzero count in prefix: min', nz.min(), 'median', int(np.median(nz)), 'max', nz.max())
for j in order[:6]:
    print('row', j, 'nz', nz[j], 'nonzero offsets', np.where(pre[j]!=0)[0].tolist(), 'vals', pre[j][pre[j]!=0].tolist())
    print('   ', pre[j].tobytes().hex(' '))
# periodicity score: columns at same phase mod p should have similar constancy
print()
print('period p : phase-wise constancy correlation (mean |const-col fraction|)')
for p in range(4, 25):
    fr = []
    for ph in range(p):
        cols = pre[:, ph::p]
        c = (cols.std(axis=0) == 0).mean()
        fr.append(c)
    print(f'  p={p:2d} constcol_frac_by_phase mean={np.mean(fr):.3f} min={np.min(fr):.3f} nphases={p}')
