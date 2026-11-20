import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_c = core['load_payload']('client', 21); raw_s = core['load_payload']('server', 21)
H, n, Sc, Ss = 14, 48413, 38, 181
mc = np.frombuffer(raw_c, np.uint8, H+n*Sc)[H:].reshape(n, Sc)
ms = np.frombuffer(raw_s, np.uint8, H+n*Ss)[H:].reshape(n, Ss)
scti = mc[:,3:7].copy().view('<u4').ravel()
lat = mc[:,17:21].copy().view('<f4').ravel()
lon = mc[:,21:25].copy().view('<f4').ravel()
# city
raw2 = core['load_payload']('client', 2)
m2 = np.frombuffer(raw2, np.uint8, 14+56293*43)[14:].reshape(56293,43)
clat = m2[:,1:5].copy().view('<f4').ravel()
clon = m2[:,5:9].copy().view('<f4').ravel()
cnti = m2[:,10:14].copy().view('<u4').ravel()
# stadium's Scti as city ordinal: compare coords
ok = (scti < 56293)
d_lat = np.abs(lat[ok] - clat[scti[ok]])
d_lon = np.abs(lon[ok] - clon[scti[ok]])
print('rows', ok.sum())
print('lat exact-equal rate', float((d_lat == 0).mean()), 'median', float(np.median(d_lat)))
print('lon exact-equal rate', float((d_lon == 0).mean()), 'median', float(np.median(d_lon)))
both = (d_lat == 0) & (d_lon == 0)
print('both equal', float(both.mean()))
print('within 0.05 deg both', float(((d_lat<0.05)&(d_lon<0.05)).mean()))
print('stadium lat=0 rows', int((lat==0).sum()), 'city lat[ordinal of those] zero?', float((clat[scti][lat==0]==0).mean()))
print('sample', list(zip(scti[:6].tolist(), lat[:6].tolist(), clat[scti[:6]].tolist(), lon[:6].tolist(), clon[scti[:6]].tolist())))
