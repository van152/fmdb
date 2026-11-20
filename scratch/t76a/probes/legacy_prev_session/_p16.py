import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21); raw_c = core['load_payload']('client', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
mc = np.frombuffer(raw_c, np.uint8, H+n*38)[H:].reshape(n,38)
pre = ms[:, :143]
def u16(m, o): return np.ascontiguousarray(m[:, o:o+2]).view('<u2').ravel()
print('== year-like u16 offsets (frac in 1850..2035) ==')
for o in range(0, 179):
    a = u16(ms, o)
    fr = float(((a>=1850)&(a<=2035)).mean())
    if fr > 0.30:
        print(f'  u16@{o:3d} yearlike={fr:.3f} min={a.min()} max={a.max()} d={len(np.unique(a))}')
print('== doy-like u16 offsets (frac in 1..366) ==')
for o in range(0, 179):
    a = u16(ms, o)
    fr = float(((a>=1)&(a<=366)).mean())
    if fr > 0.90 and o not in ():
        print(f'  u16@{o:3d} doylike={fr:.3f} min={a.min()} max={a.max()} d={len(np.unique(a))}')
