import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
def u32(o):
    return np.ascontiguousarray(ms[:, o:o+4]).view('<u4').ravel()
print('== capacity-lane candidates: u32 <= 200000 (or 0xffffffff) ==')
for o in range(0, 60):
    a = u32(o)
    ok = (a==0xffffffff) | (a <= 200000)
    if ok.mean() > 0.995:
        ff = int((a==0xffffffff).sum()); nz = int(((a>0)&(a<=200000)).sum())
        print(f'  u32@{o:3d} okrate={ok.mean():.4f} ff={ff} nonzero={nz} max={int(a[a!=0xffffffff].max()) if nz else None} nuniq={len(np.unique(a))}')
print()
print('== nonzero min/max for offsets 0..20 ==')
for o in range(0, 21):
    a = u32(o)
    print(f'  u32@{o:2d} min={a.min()} max={a.max()} ff={int((a==0xffffffff).sum())} z={int((a==0).sum())} d={len(np.unique(a))}')
