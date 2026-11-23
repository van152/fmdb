import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
def u16(o): return np.ascontiguousarray(ms[:, o:o+2]).view('<u2').ravel()
def u8(o): return ms[:, o]
print('== enum-candidate bytes 30..40 exact histograms ==')
for o in range(28, 42):
    u,c = np.unique(u8(o), return_counts=True)
    print(f'  @{o}: n={len(u)}', dict(zip(u.tolist(), c.tolist())) if len(u)<=12 else f'{u[:6].tolist()}...')
print()
print('== date pairs ==')
def date_ok(d_o, y_o):
    d = u16(d_o); y = u16(y_o)
    leap = ((y%4==0)&(y%100!=0))|(y%400==0)
    return int(((d>=1)&(d<=np.where(leap,366,365))&(y>=1700)&(y<=2035)).sum())
for d_o, y_o in ((37,39),(41,43),(45,47),(131,133),(135,137),(156,158)):
    y = u16(y_o); d = u16(d_o)
    print(f'  ({d_o},{y_o}) ok={date_ok(d_o,y_o)}/{n} y1900={int((y==1900).sum())} y<1901={int((y<1901).sum())} ymin={y.min()} ymax={y.max()} doy[min,max]=[{d.min()},{d.max()}]')
print()
print('== year value top-15 at @39 ==')
u,c = np.unique(u16(39), return_counts=True)
idx = np.argsort(-c)[:15]
print([(int(u[i]),int(c[i])) for i in idx])
print('== year top-10 @43, @47, @133, @137 ==')
for o in (43,47,133,137):
    u,c = np.unique(u16(o), return_counts=True)
    idx = np.argsort(-c)[:8]
    print(f'  @{o}', [(int(u[i]),int(c[i])) for i in idx])
