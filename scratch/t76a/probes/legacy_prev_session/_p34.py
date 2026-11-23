import runpy, sys, struct, itertools
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
def u16(o): return np.ascontiguousarray(ms[:, o:o+2]).view('<u2').ravel().astype(np.int64)
def u32(o): return np.ascontiguousarray(ms[:, o:o+4]).view('<u4').ravel().astype(np.int64)
pairs = {'A':(37,39),'B':(41,43),'C':(45,47),'D':(131,133),'E':(135,137)}
D = {k: u16(y)*400 + u16(d) for k,(d,y) in pairs.items()}
V = {k: (u16(pairs[k][1]) > 1900) for k in pairs}
print('non-null counts', {k:int(V[k].sum()) for k in pairs})
for a,b in itertools.permutations(pairs,2):
    m = V[a]&V[b]
    print(f'  {a}<={b}: {(D[a][m]<=D[b][m]).mean():.4f} (n={int(m.sum())})')
print()
print('== A (most populated) sample years ==', np.unique(u16(39)[V['A']])[:10], 'max', u16(39).max())
print('== capacity lane null/sentinel semantics ==')
for o in (0,4,8,12,16,21):
    a = u32(o)
    print(f'  @{o:2d} sentinel_ff={int((a==0xffffffff).sum())} zero={int((a==0).sum())} nonzero_pos={int(((a>0)&(a!=0xffffffff)).sum())} max={int(a[a!=0xffffffff].max())}')
