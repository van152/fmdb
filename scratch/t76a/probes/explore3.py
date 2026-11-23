import runpy, sys
import numpy as np
sys.path.insert(0, 'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_c = core['load_payload']('client', 21)
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
mc = np.frombuffer(raw_c, np.uint8, H + n * 38)[H:].reshape(n, 38)
ms = np.frombuffer(raw_s, np.uint8, H + n * 181)[H:].reshape(n, 181)

def u32(m, o):
    return np.ascontiguousarray(m[:, o:o + 4]).view('<u4').ravel().astype(np.int64)

def u16(m, o):
    return np.ascontiguousarray(m[:, o:o + 2]).view('<u2').ravel().astype(np.int64)

print('== client u32@7 (ff-dense) ==')
v = u32(mc, 7)
nn = v[v != 0xffffffff]
print('null', int((v == 0xffffffff).sum()), 'nonnull', nn.size, 'min', nn.min(), 'max', nn.max(), 'distinct', np.unique(nn).size)
print('  sample', np.unique(nn)[:20].tolist())
print('== client byte11 vs u32@11 ==')
u, c = np.unique(mc[:, 11], return_counts=True)
print(dict(zip(u.tolist(), c.tolist())))
print('== client @0 bit co-occurrence ==')
for b in (0, 1):
    for bit in range(8):
        r = ((mc[:, b] >> bit) & 1).mean()
        if 0 < r < 1:
            print(f'  b{b} bit{bit}: {r:.4f}')
print('== client @0..1 as u16 ==')
u, c = np.unique(u16(mc, 0), return_counts=True)
print(list(zip(u.tolist(), c.tolist())))
print('== client @12..16 const check ==')
for o in range(11, 17):
    print(f'  b{o}: distinct={np.unique(mc[:, o]).tolist()[:8]}')
print('== client f32 @17/@21 ==')
for o in (17, 21):
    f = np.ascontiguousarray(mc[:, o:o+4]).view('<f4').ravel()
    z = int((f == 0).sum())
    print(f'  @{o}: zero={z} ({z/n:.4f}) finite={int(np.isfinite(f).sum())} min={f.min():.3f} max={f.max():.3f}')
print('== client u16@3 ==', u16(mc, 3).min(), u16(mc, 3).max())
