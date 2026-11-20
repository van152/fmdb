import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_c = core['load_payload']('client', 21)
H, n, Sc = 14, 48413, 38
mc = np.frombuffer(raw_c, np.uint8, H+n*Sc)[H:].reshape(n, Sc)
ref = mc[:,7:11].copy().view('<u4').ravel()
scti = mc[:,3:7].copy().view('<u4').ravel()
lat = mc[:,17:21].copy().view('<f4').ravel(); lon = mc[:,21:25].copy().view('<f4').ravel()
m = ref != 0xffffffff
print('non-null', int(m.sum()), 'range', ref[m].min(), ref[m].max(), 'n>=n', int((ref[m]>=n).sum()))
# self-reference test: does referenced row share city/coords?
r = ref[m]
same_city = (scti[m] == scti[r])
d = np.maximum(np.abs(lat[m]-lat[r]), np.abs(lon[m]-lon[r]))
print('same Scti as referenced row:', float(same_city.mean()))
print('coords within 1e-6:', float((d<1e-6).mean()), 'within .05:', float((d<0.05).mean()), 'median', float(np.median(d)))
rng = np.random.default_rng(11)
idx = rng.integers(0, n, int(m.sum()))
print('control random idx: same Scti', float((scti[m]==scti[idx]).mean()), 'within .05', float((np.maximum(np.abs(lat[m]-lat[idx]),np.abs(lon[m]-lon[idx]))<0.05).mean()))
ctrl = (ref[m]+1) % n
print('control +1: same Scti', float((scti[m]==scti[ctrl]).mean()), 'within .05', float((np.maximum(np.abs(lat[m]-lat[ctrl]),np.abs(lon[m]-lon[ctrl]))<0.05).mean()))
# distribution of ref values relative to own ordinal
j = np.where(m)[0]
rel = (ref[m].astype(np.int64) - j)
print('ref - own ordinal: unique', len(np.unique(rel)), 'min', rel.min(), 'max', rel.max(), 'sample', rel[:10].tolist())
