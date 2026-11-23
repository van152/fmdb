import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
def u16(o): return np.ascontiguousarray(ms[:, o:o+2]).view('<u2').ravel()
def u32(o): return np.ascontiguousarray(ms[:, o:o+4]).view('<u4').ravel()
import datetime
def date_ok(doy_o, yr_o):
    d = u16(doy_o); y = u16(yr_o)
    bad = 0
    for i in range(0, n, 1):
        pass
    # vectorized: max doy for year
    leap = ((y % 4 == 0) & (y % 100 != 0)) | (y % 400 == 0)
    maxd = np.where(leap, 366, 365)
    return int(((d >= 1) & (d <= maxd) & (y >= 1800) & (y <= 2035)).sum())
for doy_o, yr_o in ((37,39),(41,43),(45,47),(33,35),(36,38),(40,42),(44,46)):
    print(f'date cand doy@{doy_o} year@{yr_o}: ok {date_ok(doy_o,yr_o)}/{n}')
print()
print('capacity relations:')
c = {o: u32(o) for o in range(0,25)}
for a in (0,4,8,12,16,21):
    for b in (0,4,8,12,16,21):
        if a>=b: continue
        A,B = c[a], c[b]
        m = (A!=0xffffffff)&(B!=0xffffffff)
        le = float(((A[m]<=B[m])).mean())
        if le > 0.97 or le < 0.03:
            print(f'  u32@{a} <= u32@{b}: {le:.4f} (n={int(m.sum())})')
