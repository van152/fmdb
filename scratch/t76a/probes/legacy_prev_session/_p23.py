import runpy, sys, itertools
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
def u32(o): return np.ascontiguousarray(ms[:, o:o+4]).view('<u4').ravel()
def u16(o): return np.ascontiguousarray(ms[:, o:o+2]).view('<u2').ravel()
caps = [0,4,8,12,16,21]
print('== pairwise <= rates among capacity-like u32 lanes (excluding sentinel) ==')
for a,b in itertools.permutations(caps,2):
    A,B = u32(a), u32(b)
    m = (A!=0xffffffff)&(B!=0xffffffff)
    print(f'  @{a:2d}<={b:2d}: {((A[m]<=B[m]).mean()):.4f}  n={int(m.sum())}')
print()
print('== exact-equality rates (helps spot duplicated lanes) ==')
for a,b in itertools.combinations(caps,2):
    A,B=u32(a),u32(b); m=(A!=0xffffffff)&(B!=0xffffffff)
    print(f'  @{a:2d}=={b:2d}: {float((A[m]==B[m]).mean()):.4f}')
print()
print('== dates: ordering matrix (a<=b as (year,doy)) ==')
def key(o): return (u16(o+2).astype(np.int64)*512 + u16(o))
D = {o: key(o) for o in (37,41,45,131,135)}
for a,b in itertools.permutations(D,2):
    print(f'  d{a}<==d{b}: {float((D[a]<=D[b]).mean()):.4f}')
print()
for o in (37,41,45,131,135):
    y=u16(o+2); d=u16(o)
    print(f'  lane doy@{o} year@{o+2}: null(year<1901)={int((y<1901).sum())} minyear={y.min()} maxyear={y.max()}')
