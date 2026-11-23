import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21); raw_c = core['load_payload']('client', 21)
raw2 = core['load_payload']('client', 2)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
mc = np.frombuffer(raw_c, np.uint8, H+n*38)[H:].reshape(n,38)
m2 = np.frombuffer(raw2, np.uint8, 14+56293*43)[14:].reshape(56293,43)
cnti2 = m2[:,10:14].copy().view('<u4').ravel()
scti = mc[:,3:7].copy().view('<u4').ravel()
exp = cnti2[scti]
print('expected nation domain', exp.min(), exp.max(), len(np.unique(exp)))
def test(name, col):
    m = np.isin(col, np.unique(exp))
    # also exact agreement count
    agree = float((col == exp).mean())
    print(f'{name}: values in nation-domain {m.mean():.4f} agree-with-expected {agree:.4f}')
for o in range(0, 40):
    test(f'u8@{o:3d}', ms[:, o])
