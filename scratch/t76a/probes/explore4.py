import runpy, sys
import numpy as np
sys.path.insert(0, 'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H + n * 181)[H:].reshape(n, 181)
S = ms[:, :143]

def u32(m, o):
    return np.ascontiguousarray(m[:, o:o + 4]).view('<u4').ravel().astype(np.int64)

def u16(m, o):
    return np.ascontiguousarray(m[:, o:o + 2]).view('<u2').ravel().astype(np.int64)

print('=== server-only 143B: aligned u32 sweep (4-byte grid) ===')
print('off  distinct  null_ff  null0  min..max   |f32 ok')
for o in range(0, 143 - 3, 1):
    v = u32(S, o)
    d = np.unique(v).size
    nff = int((v == 0xffffffff).sum())
    nz = int((v == 0).sum())
    f = np.ascontiguousarray(S[:, o:o+4]).view('<f4').ravel()
    fin = np.isfinite(f)
    okf = bool(fin.all() and (np.abs(f[fin]) < 1e6).all())
    tag = ''
    if d <= 12: tag = ' <<const/small'
    print(f'{o:3d} {d:7d} {nff:7d} {nz:6d}  {v.min():10d}..{v.max():10d} | {okf}{tag}')
