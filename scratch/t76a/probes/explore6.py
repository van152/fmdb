import runpy, sys
import numpy as np
sys.path.insert(0, 'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H + n * 181)[H:].reshape(n, 181)
S = ms[:, :143]

def U(m, o, w):
    return np.ascontiguousarray(m[:, o:o + w]).view(f'<u{w}').ravel().astype(np.int64)

print('=== server-only 143B, 4-aligned u32 ===')
for o in range(0, 140, 4):
    v = U(S, o, 4)
    nn = v[v != 0xffffffff]
    print(f'@{o:3d} u32 d={np.unique(v).size:5d} ff={int((v==0xffffffff).sum()):6d} z={int((v==0).sum()):6d} '
          f'min={v.min():10d} max={v.max():10d} | nonnull min={nn.min() if nn.size else 0} max={nn.max() if nn.size else 0}')
print('\n=== 4-aligned u16 ===')
for o in range(0, 142, 4):
    v = U(S, o, 2)
    print(f'@{o:3d} u16 d={np.unique(v).size:5d} ff={int((v==0xffff).sum()):6d} z={int((v==0).sum()):6d} min={v.min():6d} max={v.max():6d}')
print('\n=== byte columns 0..142: distinct / const ===')
for o in range(143):
    c = S[:, o]
    u = np.unique(c)
    if u.size <= 16:
        print(f'  b{o:3d} d={u.size:3d} {u.tolist()}')
