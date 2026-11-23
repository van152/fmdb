import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21); raw_c = core['load_payload']('client', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
mc = np.frombuffer(raw_c, np.uint8, H+n*38)[H:].reshape(n,38)
def u32(o,m=ms): return np.ascontiguousarray(m[:,o:o+4]).view('<u4').ravel().astype(np.int64)
own = u32(16); lat = np.ascontiguousarray(ms[:,160:164]).view('<f4').ravel(); lon = np.ascontiguousarray(ms[:,164:168]).view('<f4').ravel()
scti = u32(3, mc); cap = u32(0)
vals, cnts = np.unique(own, return_counts=True)
rep = vals[(cnts>=3)&(vals!=0xffffffff)]
print('repeated @16 values (>=3):', len(rep))
shown=0
for v in rep:
    idx = np.where(own==v)[0]
    la, lo = lat[idx], lon[idx]
    spread = float(np.sqrt(((la-la.mean())*111)**2 + ((lo-lo.mean())*111*np.cos(np.radians(la.mean())))**2).max())
    if spread < 5 and shown < 8:
        shown += 1
        print(f'\n@16={int(v)} n={len(idx)} spread={spread:.2f}km')
        for j in idx[:8]:
            print(f'   row {j:6d} Scti={scti[j]:6d} cap={cap[j]:7d} lat={lat[j]:.5f} lon={lon[j]:.5f}')
