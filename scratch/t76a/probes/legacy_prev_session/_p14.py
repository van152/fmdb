import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n, Ss = 14, 48413, 181
ms = np.frombuffer(raw_s, np.uint8, H+n*Ss)[H:].reshape(n, Ss)
pre = ms[:, 0:143]
print('offset u8d const? u16[min,max] u32[min,max,d] ff0 zero')
for off in range(143):
    col = pre[:, off]
    u = np.unique(col)
    s = f"{off:4d} u8d={len(u):3d}"
    if len(u)<=3: s += f" u8={u.tolist()}"
    if off+2 <= 143:
        v = pre[:, off:off+2].copy().view('<u2').ravel()
        s += f" u16[{v.min()},{v.max()}]d{len(np.unique(v))}"
    if off+4 <= 143:
        v = pre[:, off:off+4].copy().view('<u4').ravel()
        f = pre[:, off:off+4].copy().view('<f4').ravel()
        s += f" u32[{v.min()},{v.max()}]d{len(np.unique(v))} ff{int((v==0xffffffff).sum())} z{int((v==0).sum())}"
        if np.isfinite(f).all() and np.abs(f).max()<1e6:
            s += f" F32[{f.min():.4g},{f.max():.4g}]"
    print(s)
