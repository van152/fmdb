import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
def u16(o): return np.ascontiguousarray(ms[:, o:o+2]).view('<u2').ravel()
print('== u16 lanes with pitch-dimension-like domains ==')
for o in range(0, 168):
    a = u16(o).astype(np.int64)
    dm = float(((a>=60)&(a<=130)).mean())
    dcm = float(((a>=600)&(a<=1300)).mean())
    if dm > 0.5 or dcm > 0.5:
        print(f'  u16@{o:3d} metres60-130={dm:.3f} decimetres600-1300={dcm:.3f} min={a.min()} max={a.max()} d={len(np.unique(a))} top={np.unique(a, return_counts=True)[0][-5:].tolist()}')
print()
for o in (25,27,49,50,51,52,58,60):
    u,c = np.unique(u16(o), return_counts=True)
    print(f'u16@{o}: n={len(u)} min={u.min()} max={u.max()}', dict(zip(u.tolist(),c.tolist())) if len(u)<=14 else 'top: '+str([(int(u[i]),int(c[i])) for i in np.argsort(-c)[:8]]))
