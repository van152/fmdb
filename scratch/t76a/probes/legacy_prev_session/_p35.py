import runpy, sys, itertools
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
def u16(o): return np.ascontiguousarray(ms[:, o:o+2]).view('<u2').ravel().astype(np.int64)
pairs = {'A':(37,39),'B':(41,43),'C':(45,47),'D':(131,133),'E':(135,137)}
def days(k):
    d = u16(pairs[k][0]); y = u16(pairs[k][1])
    return y*365 + d
V = {k: (u16(pairs[k][1]) > 1900) for k in pairs}
for a,b in (('A','B'),('A','C'),('A','D'),('C','B'),('B','D'),('D','E')):
    m = V[a]&V[b]
    delta = (days(b)-days(a))[m]
    print(f'{a}->{b}: n={int(m.sum())} min={delta.min()} p50={np.percentile(delta,50):.0f} p95={np.percentile(delta,95):.0f} max={delta.max()} neg={int((delta<0).sum())}')
print()
print('== exact day-granularity: is there a date where doy+year look like a "relay" pair (delta 1..3y)? ==')
m = V['A']&V['B']
print('histogram of delta years (A->B) quantized:', np.unique((days('B')-days('A'))[m]//365, return_counts=True))
