import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
pre = ms[:, :168]
print('off | u8uniq | small set (<=8) | u16uniq | u32: min,max,nsent,ndistinct')
for o in range(0, 168):
    u8 = np.unique(pre[:, o])
    parts = [f'{o:3d} {len(u8):3d}']
    if len(u8) <= 8: parts.append(str(u8.tolist()))
    else:
        if o+2 <= 168:
            pass
    if o+2 <= 168:
        v2 = np.ascontiguousarray(pre[:, o:o+2]).view('<u2').ravel()
        u2 = np.unique(v2)
        parts.append(f'u16d={len(u2)}[{v2.min()},{v2.max()}]')
    if o+4 <= 168:
        v4 = np.ascontiguousarray(pre[:, o:o+4]).view('<u4').ravel()
        parts.append(f'u32d={len(np.unique(v4))}[{v4.min()},{v4.max()}]ff={int((v4==0xffffffff).sum())}z={int((v4==0).sum())}')
    print(' '.join(parts))
