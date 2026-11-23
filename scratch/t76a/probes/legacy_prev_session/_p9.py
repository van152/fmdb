import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_c = core['load_payload']('client', 21)
H, n, Sc = 14, 48413, 38
mc = np.frombuffer(raw_c, np.uint8, H+n*Sc)[H:].reshape(n, Sc)
scti = mc[:,3:7].copy().view('<u4').ravel()
lat = mc[:,17:21].copy().view('<f4').ravel(); lon = mc[:,21:25].copy().view('<f4').ravel()
raw2 = core['load_payload']('client', 2)
m2 = np.frombuffer(raw2, np.uint8, 14+56293*43)[14:].reshape(56293,43)
clat = m2[:,1:5].copy().view('<f4').ravel(); clon = m2[:,5:9].copy().view('<f4').ravel()
has = (lat != 0) | (lon != 0)
print('rows with coords', int(has.sum()))
def score(idx):
    ok = has & (idx < 56293)
    d = np.maximum(np.abs(lat[ok]-clat[idx[ok]]), np.abs(lon[ok]-clon[idx[ok]]))
    return float((d < 0.05).mean()), float(np.median(d)), int(ok.sum())
rng = np.random.default_rng(7)
print('real Scti      ', score(scti))
print('shift +1       ', score((scti+1) % 56293))
print('shift +7       ', score((scti+7) % 56293))
print('shift +1000    ', score((scti+1000) % 56293))
print('random perm    ', score(rng.permutation(56293)[scti % 56293] if False else rng.integers(0,56293,n)))
uids2 = m2[:,34:38].copy().view('<u4').ravel()
# UID-join control: map city UID->row
import collections
u2r = {}
for r_,u in enumerate(uids2.tolist()):
    u2r.setdefault(u, r_)
print('city UID->row map size', len(u2r), 'dup uids', len(uids2)-len(u2r))
rowmap = np.array([u2r.get(int(v), 10**9) for v in scti], dtype=np.int64)
print('Scti as city UID  ', score(rowmap))
