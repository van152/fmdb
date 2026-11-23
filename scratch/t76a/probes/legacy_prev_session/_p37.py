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
scti = np.ascontiguousarray(mc[:,3:7]).view('<u4').ravel().astype(np.int64)
clat = np.ascontiguousarray(m2[:,1:5]).view('<f4').ravel(); clon = np.ascontiguousarray(m2[:,5:9]).view('<f4').ravel()
lat = np.ascontiguousarray(mc[:,17:21]).view('<f4').ravel(); lon = np.ascontiguousarray(mc[:,21:25]).view('<f4').ravel()
def u16(o,m=ms): return np.ascontiguousarray(m[:,o:o+2]).view('<u2').ravel().astype(np.int64)
def u32(o,m=ms): return np.ascontiguousarray(m[:,o:o+4]).view('<u4').ravel().astype(np.int64)
has = (lat!=0)|(lon!=0)
print('== client u16@4 vs nation ordinals from city Cnti ==')
exp = m2[:,10].astype(np.int64)[scti]
for o in (4,):
    a = u16(o, mc)
    print(f'  u16@{o} agree with city Cnti: {float((a[has]==exp[has]).mean()):.4f}; in 0..249: {float(((a>=0)&(a<=249)).mean()):.4f}')
print('== server @16 (non-ff): identity test ==')
s16 = u32(16); m = s16 != 0xffffffff
print('  @16 == Scti?', float((s16[m]==scti[m]).mean()))
print('  @16 in city-ordinal range', float((s16[m]<56293).mean()))
d = np.maximum(np.abs(lat[m]-clat[np.minimum(s16[m],56292)]), np.abs(lon[m]-clon[np.minimum(s16[m],56292)]))
print('  @16 as city ordinal -> coord within .05deg', float((d<0.05).mean()))
rng=np.random.default_rng(5); ctl=rng.integers(0,56293,int(m.sum()))
dc = np.maximum(np.abs(lat[m]-clat[ctl]), np.abs(lon[m]-clon[ctl]))
print('  control random city ordinal  -> coord within .05deg', float((dc<0.05).mean()))
print('  @16 values <250:', int((s16[m]<250).sum()), 'of', int(m.sum()))
print()
print('== date lane year histograms ==')
for name,(d_,y_) in {'A':(37,39),'B':(41,43),'C':(45,47),'D':(131,133),'E':(135,137)}.items():
    y = u16(y_); d = u16(d_)
    v = y>1900
    print(f'  {name} doy@{d_} yr@{y_}: n={int(v.sum())} ymin={y[v].min()} ymax={y[v].max()} yp10={int(np.percentile(y[v],10))} yp50={int(np.percentile(y[v],50))}')
