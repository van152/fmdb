import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21); raw_c = core['load_payload']('client', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
mc = np.frombuffer(raw_c, np.uint8, H+n*38)[H:].reshape(n,38)
def u16(o,m=ms): return np.ascontiguousarray(m[:,o:o+2]).view('<u2').ravel().astype(np.int64)
def u32(o,m=ms): return np.ascontiguousarray(m[:,o:o+4]).view('<u4').ravel().astype(np.int64)
print('== date lanes: future-year counts (year > 2026) ==')
for name,(d_,y_) in {'A@37':(37,39),'B@41':(41,43),'C@45':(45,47),'D@131':(131,133),'E@135':(135,137)}.items():
    y = u16(y_); v = y>1900
    print(f'  {name}: nonnull={int(v.sum())} future(>2026)={int((y>2026).sum())} eq1900={int((y==1900).sum())} yr[min,max]=[{y[v].min()},{y[v].max()}]')
print()
print('== capacity @4 vs @0 among rows where @4!=0 ==')
a0, a4 = u32(0), u32(4)
m = a4 != 0
print('  n(@4!=0)', int(m.sum()), '@4==@0 rate', float((a4[m]==a0[m]).mean()), '@4<@0 rate', float((a4[m]<a0[m]).mean()))
print('  @0==@4 overall', float((a0==a4).mean()))
print('  rows where @4>0 and @0==0:', int(((a4>0)&(a0==0)).sum()))
print()
print('== @16 domain checks ==')
s16 = u32(16); m16 = s16 != 0xffffffff
print('  nonnull', int(m16.sum()), 'min', int(s16[m16].min()), 'max', int(s16[m16].max()), 'zero', int((s16==0).sum()))
for lim,name in ((84259,'club t3'),(84507,'team t24'),(56293,'city t2'),(48413,'stadium t21'),(7047,'comp t25'),(278,'t23')):
    print(f'  in {name} ordinal range: {float((s16[m16]<lim).mean()):.4f}')
print()
print('== client byte11 vs city nation (Cnti of Scti) ==')
raw2 = core['load_payload']('client', 2)
m2 = np.frombuffer(raw2, np.uint8, 14+56293*43)[14:].reshape(56293,43)
scti = u32(3, mc)
cnti = m2[:,10].astype(np.int64)[scti]
import collections
tab = collections.defaultdict(collections.Counter)
for b,cv in zip(mc[:,11].tolist(), cnti.tolist()):
    tab[b][cv]+=1
for b in sorted(tab):
    tot = sum(tab[b].values())
    top = tab[b].most_common(3)
    print(f'  byte11={b:3d} n={tot:6d} top nations {[(k,v) for k,v in top]}')
