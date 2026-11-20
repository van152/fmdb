import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_c = core['load_payload']('client', 21); raw_s = core['load_payload']('server', 21)
raw2 = core['load_payload']('client', 2)
H, n = 14, 48413
mc = np.frombuffer(raw_c, np.uint8, H+n*38)[H:].reshape(n,38)
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
m2 = np.frombuffer(raw2, np.uint8, 14+56293*43)[14:].reshape(56293,43)
scti = np.ascontiguousarray(mc[:,3:7]).view('<u4').ravel().astype(np.int64)
lat = np.ascontiguousarray(mc[:,17:21]).view('<f4').ravel()
lon = np.ascontiguousarray(mc[:,21:25]).view('<f4').ravel()
has = (lat != 0) | (lon != 0)
city = {
 'Cnti_u8@10': m2[:,10].astype(np.int64),
 'Catt_u8@9': m2[:,9].astype(np.int64),
 'Cwea_u32@14': np.ascontiguousarray(m2[:,14:18]).view('<u4').ravel().astype(np.int64),
 'Clri_u32@25': np.ascontiguousarray(m2[:,25:29]).view('<u4').ravel().astype(np.int64),
 'Clgi_u32@21': np.ascontiguousarray(m2[:,21:25]).view('<u4').ravel().astype(np.int64),
}
print('city lane domains:')
for k,v in city.items(): print(' ', k, 'min',v.min(),'max',v.max(),'d',len(np.unique(v)))
def lanes(m):
    out={}
    for o in range(m.shape[1]-(13)):
        for w,fmt in ((1,None),(2,'<u2'),(4,'<u4')):
            if o+w>m.shape[1]-13: continue
            col = m[:,o].astype(np.int64) if w==1 else np.ascontiguousarray(m[:,o:o+w]).view(fmt).ravel().astype(np.int64)
            out[(o,w)] = col
    return out
for name, mm in (('client',mc),('server',ms)):
    print(f'== {name} ==')
    L = lanes(mm)
    for ck, cvec in city.items():
        exp = cvec[scti]
        best = sorted(((float((L[k][has]==exp[has]).mean()), k) for k in L), reverse=True)[:3]
        print(f'  {ck:12s} best lanes: ' + ', '.join(f'u{k[1]*8}@{k[0]}={v:.4f}' for v,k in best))
