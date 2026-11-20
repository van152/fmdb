import runpy, sys, json
import numpy as np
sys.path.insert(0, 'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_c = core['load_payload']('client', 21)
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
mc = np.frombuffer(raw_c, np.uint8, H + n * 38)[H:].reshape(n, 38)
ms = np.frombuffer(raw_s, np.uint8, H + n * 181)[H:].reshape(n, 181)
print('lens', len(raw_c), len(raw_s), 'closure', 14 + n * 38 + 8, 14 + n * 181 + 8)

def u32(m, o):
    return np.ascontiguousarray(m[:, o:o + 4]).view('<u4').ravel().astype(np.uint64)

def u16(m, o):
    return np.ascontiguousarray(m[:, o:o + 2]).view('<u2').ravel().astype(np.int64)

print('\n=== client 38B per-offset ===')
print('off u8d  zero%   ff%   | u16min u16max | u32min u32max nff | f32 plausible')
for o in range(38):
    c = mc[:, o]
    row = f'{o:3d} {np.unique(c).size:4d} {(c==0).mean():.3f} {(c==0xff).mean():.3f}'
    if o + 2 <= 38:
        v = u16(mc, o)
        row += f' | {v.min():6d} {v.max():6d}'
    else:
        row += ' |      -      -'
    if o + 4 <= 38:
        v = u32(mc, o)
        row += f' | {v.min():10d} {v.max():10d} {int((v==0xffffffff).sum()):5d}'
        f = np.ascontiguousarray(mc[:, o:o+4]).view('<f4').ravel()
        fin = np.isfinite(f)
        ok = fin.all() and (np.abs(f[fin]) < 1e9).all()
        row += f' | {ok} {float(f[fin].min()):.4g}/{float(f[fin].max()):.4g}' if fin.any() else ' | -'
    else:
        row += ' |          -          -     -'
    print(row)
