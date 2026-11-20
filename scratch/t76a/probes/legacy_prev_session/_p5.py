import runpy, sys, json
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_c = core['load_payload']('client', 21)
raw_s = core['load_payload']('server', 21)
H, n, Sc, Ss = 14, 48413, 38, 181
mc = np.frombuffer(raw_c, dtype=np.uint8, count=H+n*Sc)[H:].reshape(n, Sc)
ms = np.frombuffer(raw_s, dtype=np.uint8, count=H+n*Ss)[H:].reshape(n, Ss)
print('--- client field bytes 0..24 exact u8 histograms ---')
for off in range(25):
    u, c = np.unique(mc[:, off], return_counts=True)
    if len(u) <= 24:
        print(off, dict(zip(u.tolist(), c.tolist())))
    else:
        print(off, 'distinct', len(u), 'top', dict(zip(u[-1:].tolist(), c[-1:].tolist())), 'nzero', int((mc[:,off]==0).sum()))
print('--- sample client rows 0..5 (hex) with f32 at 17,21 ---')
for j in range(6):
    r = mc[j]
    print(j, r.hex(' '), 'Slat', r[17:21].copy().view('<f4')[0], 'Slon', r[21:25].copy().view('<f4')[0])
