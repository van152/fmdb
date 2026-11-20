import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21); raw_c = core['load_payload']('client', 21)
raw2 = core['load_payload']('client', 2)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
mc = np.frombuffer(raw_c, np.uint8, H+n*38)[H:].reshape(n,38)
m2 = np.frombuffer(raw2, np.uint8, 14+56293*43)[14:].reshape(56293,43)
cnti2 = m2[:,10:14].copy().view('<u4').ravel()
scti = mc[:,3:7].copy().view('<u4').ravel()
exp = cnti2[scti]
lat = mc[:,17:21].copy().view('<f4').ravel(); lon = mc[:,21:25].copy().view('<f4').ravel()
has = (lat != 0) | (lon != 0)
print('== expected nation (from city of Scti): agreement by lane ==')
res=[]
for o in range(0, 168):
    for w,fmt in ((1,None),(2,'<u2'),(4,'<u4')):
        if o+w > 168: continue
        col = np.ascontiguousarray(ms[:, o:o+w]).view(fmt).ravel().astype(np.int64) if w>1 else ms[:,o].astype(np.int64)
        ag = float((col[has]==exp[has]).mean())
        res.append((ag, o, w))
res.sort(reverse=True)
for ag,o,w in res[:12]:
    print(f'  u{w*8}@{o:3d} agree={ag:.4f}')
print()
print('== client lanes same test (client 0..24) ==')
res2=[]
for o in range(0, 26):
    for w,fmt in ((1,None),(2,'<u2'),(4,'<u4')):
        if o+w > 26: continue
        col = np.ascontiguousarray(mc[:, o:o+w]).view(fmt).ravel().astype(np.int64) if w>1 else mc[:,o].astype(np.int64)
        ag = float((col[has]==exp[has]).mean())
        res2.append((ag,o,w))
res2.sort(reverse=True)
for ag,o,w in res2[:10]:
    print(f'  u{w*8}@{o:3d} agree={ag:.4f}')
