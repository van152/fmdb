import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
def u16(o): return np.ascontiguousarray(ms[:, o:o+2]).view('<u2').ravel().astype(np.int64)
def u32(o): return np.ascontiguousarray(ms[:, o:o+4]).view('<u4').ravel().astype(np.int64)
a, b = u16(25), u16(27); c, d = u16(58), u16(60)
print('@25==@58', float((a==c).mean()), '@27==@60', float((b==d).mean()))
print('both equal', float(((a==c)&(b==d)).mean()))
print('@58==0 count', int((c==0).sum()), '@25==0', int((a==0).sum()))
print('@25>@27', float((a>b).mean()), ' @58>@60', float((c>d).mean()))
print()
print('== proper pairwise clustering of @16 groups ==')
lat = np.ascontiguousarray(ms[:,160:164]).view('<f4').ravel()
lon = np.ascontiguousarray(ms[:,164:168]).view('<f4').ravel()
own = u32(16); m = own != 0xffffffff
vals, cnts = np.unique(own[m], return_counts=True)
rep = vals[cnts>=2]
mx = []
for v in rep[:600]:
    idx = np.where(own==v)[0]
    if len(idx) < 2: continue
    la = lat[idx]; lo = lon[idx]
    dlat = (la[:,None]-la[None,:])*111.0
    dlon = (lo[:,None]-lo[None,:])*111.0*np.cos(np.radians(la[:,None]))
    dist = np.sqrt(dlat**2+dlon**2)
    mx.append(float(dist.max()))
mx = np.array(mx)
print(f'groups tested {len(mx)}: median max-pairwise-dist {np.median(mx):.1f} km, p90 {np.percentile(mx,90):.1f}, frac<60km {float((mx<60).mean()):.3f}, frac<200km {float((mx<200).mean()):.3f}')
rng=np.random.default_rng(4); ctl=[]
for v in rep[:600]:
    idx = np.where(own==v)[0]
    k = len(idx)
    pick = rng.integers(0,n,k)
    la = lat[pick]; lo = lon[pick]
    dlat=(la[:,None]-la[None,:])*111.0; dlon=(lo[:,None]-lo[None,:])*111.0*np.cos(np.radians(la[:,None]))
    ctl.append(float(np.sqrt(dlat**2+dlon**2).max()))
ctl=np.array(ctl)
print(f'control: median {np.median(ctl):.1f} km, frac<60km {float((ctl<60).mean()):.3f}')
print()
print('== per-group same-Scti (proper) ==')
scti = u32(3)
same=[]
for v in rep[:600]:
    idx=np.where(own==v)[0]
    same.append(len(set(scti[idx].tolist()))==1)
print('same-city groups:', float(np.mean(same)))
