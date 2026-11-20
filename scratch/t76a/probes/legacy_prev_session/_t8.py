import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy'); n = len(rows)
starts = rows[:,0].astype(np.int64); lens = rows[:,1].astype(np.int64)
def col(o, w=2):
    ok = (o + w <= lens - 13)
    out = np.full(n, -1, dtype=np.int64)
    idx = np.where(ok)[0]
    for j in idx:
        out[j] = int.from_bytes(raw[starts[j]+o: starts[j]+o+w], 'little')
    return out, ok
print('row count', n, 'min len', lens.min())
for o in range(0, 20, 2):
    v, ok = col(o)
    u = np.unique(v[ok])
    print(f'  u16@{o:2d} fill={ok.mean():.3f} d={len(u)} min={v[ok].min()} max={v[ok].max()} sample={u[:8].tolist()}')
print()
# date pair interpretation: does (doy@0, year@2) hold? check year domain
for (d_, y_) in ((0,2),(4,6),(8,10),(12,14)):
    d, okd = col(d_); y, oky = col(y_)
    m = okd & oky
    leap = ((y%4==0)&(y%100!=0))|(y%400==0)
    good = ((d>=0)&(d<=np.where(leap,366,365))&(y>=1800)&(y<=2035))
    print(f'  date({d_},{y_}): ok={int(good[m].sum())}/{int(m.sum())} y1900={int((y[m]==1900).sum())} yd={len(np.unique(y[m]))}')
