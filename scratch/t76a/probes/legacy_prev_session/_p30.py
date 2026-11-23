import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21); raw_c = core['load_payload']('client', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
mc = np.frombuffer(raw_c, np.uint8, H+n*38)[H:].reshape(n,38)
def u32(o, m=ms): return np.ascontiguousarray(m[:, o:o+4]).view('<u4').ravel()
def u16(o, m=ms): return np.ascontiguousarray(m[:, o:o+2]).view('<u2').ravel()
own = u32(16)
non = own[own != 0xffffffff]
print('@16 non-null', len(non), 'distinct', len(np.unique(non)), 'max', non.max(), 'min', non.min())
u, c = np.unique(non, return_counts=True)
print('values with >=3 stadiums:', [(int(a),int(b)) for a,b in zip(u,c) if b>=3][:20])
print('n values used by exactly 1 stadium:', int((c==1).sum()), 'of', len(u))
# geographic clustering for repeated owner values
lat = np.ascontiguousarray(ms[:,160:164]).view('<f4').ravel()
lon = np.ascontiguousarray(ms[:,164:168]).view('<f4').ravel()
rep = [(int(a),int(b)) for a,b in zip(u,c) if b>=3]
import statistics
spreads=[]
for val,cnt in rep:
    idx = np.where(own==val)[0]
    d = np.sqrt((lat[idx]*111.0)**2 + (lon[idx]*111.0*np.cos(np.radians(lat[idx])))**2)
    spreads.append((val,cnt,float(np.median(d)),float(d.max())))
print('median cluster radius (km) for repeated owner values: median of medians %.1f' % statistics.median([s[2] for s in spreads]))
for s in spreads[:10]: print('  owner',s)
# control: random grouping of same sizes
rng=np.random.default_rng(3)
ctrl=[]
for val,cnt in rep:
    idx = rng.integers(0,n,cnt)
    d = np.sqrt((lat[idx]*111.0)**2 + (lon[idx]*111.0*np.cos(np.radians(lat[idx])))**2)
    ctrl.append(float(np.median(d)))
print('control median radius %.1f km' % statistics.median(ctrl))
