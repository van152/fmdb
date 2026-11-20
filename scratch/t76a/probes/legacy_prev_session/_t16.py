import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy'); n = len(rows)
starts = rows[:,0].astype(np.int64); lens = rows[:,1].astype(np.int64)
A = np.frombuffer(raw, np.uint8)
def c16(o): return (A[starts+o].astype(np.int64) | (A[starts+o+1].astype(np.int64)<<8))
print('== u16 domain at each even offset, all rows ==')
for o in range(0, 74, 2):
    v = c16(o); u = np.unique(v)
    s = f'{o:3d} d={len(u):5d} [{int(v.min())},{int(v.max())}]'
    if len(u) <= 8: s += f' {u.tolist()}'
    else:
        top = np.argsort(-np.unique(v, return_counts=True)[1])[:4]
        uu, cc = np.unique(v, return_counts=True)
        s += ' top ' + str([(int(uu[i]), int(cc[i])) for i in top])
    print(s)
print()
print('== date pair test allowing (0,0) null ==')
for d_o in range(0, 30, 2):
    for y_o in range(0, 30, 2):
        if y_o==d_o: continue
        d, y = c16(d_o), c16(y_o)
        leap = ((y%4==0)&(y%100!=0))|(y%400==0)
        mx = np.where(leap,366,365)
        good = ((d==0)&(y==0)) | ((d>=1)&(d<=mx)&(y>=1850)&(y<=2035))
        if good.mean() > 0.9:
            print(f'  ({d_o},{y_o}): {good.mean():.4f} nulls={int(((d==0)&(y==0)).sum())} y1900={int((y==1900).sum())}')
