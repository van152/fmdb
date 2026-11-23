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

print('=== packed-date scan (u32 = doy | year<<16) over server-only 143B ===')
for o in range(0, 140):
    v = U(S, o, 4)
    doy, yr = v & 0xFFFF, v >> 16
    ok = ((doy >= 1) & (doy <= 366) & (yr >= 1850) & (yr <= 2035))
    r = ok.mean()
    if r > 0.9:
        print(f'  @{o:3d} rate={r:.4f} doy[{doy[ok].min()},{doy[ok].max()}] yr[{yr[ok].min()},{yr[ok].max()}] zeros={int((v==0).sum())}')
print('\n=== same scan on client 25B ===')
raw_c = core['load_payload']('client', 21)
mc = np.frombuffer(raw_c, np.uint8, H + n * 38)[H:].reshape(n, 38)
for o in range(0, 22):
    v = U(mc, o, 4)
    doy, yr = v & 0xFFFF, v >> 16
    ok = ((doy >= 1) & (doy <= 366) & (yr >= 1850) & (yr <= 2035))
    if ok.mean() > 0.5:
        print(f'  client @{o:3d} rate={ok.mean():.4f}')

print('\n=== u16 const / low-card columns in server-only (every offset) ===')
for o in range(0, 142):
    v = U(S, o, 2)
    u = np.unique(v)
    if u.size <= 8:
        print(f'  u16@{o:3d} d={u.size} {u.tolist()} counts={[int((v==x).sum()) for x in u]}')

print('\n=== search 0x076C-like tags: u16 with d small and value in 1800..2000 ===')
for o in range(0, 142):
    v = U(S, o, 2)
    if np.unique(v).size <= 40 and v.min() >= 1500 and v.max() <= 2100:
        print(f'  u16@{o:3d} d={np.unique(v).size} min={v.min()} max={v.max()}')
