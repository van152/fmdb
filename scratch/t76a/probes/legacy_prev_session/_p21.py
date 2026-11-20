import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
def u16(o): return np.ascontiguousarray(ms[:, o:o+2]).view('<u2').ravel()
for o in (33,34,36,37,38,39,40,41,42,43,44,45,46,47,48,49,50):
    a = u16(o)
    print(f'u16@{o}: d={len(np.unique(a))} min={a.min()} max={a.max()} yearfrac={((a>=1800)&(a<=2035)).mean():.3f} doyfrac={((a>=1)&(a<=366)).mean():.3f} vals={np.unique(a)[:10].tolist()}')
print()
print('sample rows 0..5, offsets 33..58:')
for j in range(6):
    print(j, ms[j,33:59].tobytes().hex(' '))
    r = ms[j].tobytes()
    print('   u16s:', [(o, int(np.frombuffer(r[o:o+2],'<u2')[0])) for o in range(33,59,2)])
