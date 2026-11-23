import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
def u16(o): return np.ascontiguousarray(ms[:, o:o+2]).view('<u2').ravel().astype(np.int64)
def u32(o): return np.ascontiguousarray(ms[:, o:o+4]).view('<u4').ravel().astype(np.int64)
print('== pitch length vs width ordering ==')
for a,b in ((25,27),(58,60),(33,35),(49,50),(51,52)):
    A,B = u16(a), u16(b)
    m = (A>0)&(B>0)
    print(f'  u16@{a} vs u16@{b}: A>=B {(A[m]>=B[m]).mean():.4f} n={int(m.sum())} median A={np.median(A[m]):.0f} B={np.median(B[m]):.0f}')
print()
print('== exact value modes for dimension lanes ==')
for o in (25,27,33,35,49,50,51,58,60):
    u,c = np.unique(u16(o), return_counts=True)
    top = np.argsort(-c)[:5]
    print(f'  @{o}: ' + ', '.join(f'{int(u[i])}x{int(c[i])}' for i in top))
print()
print('== stadium sides: sum of 8 u32 at 64+8k vs capacity lanes ==')
tot = sum(u32(64+8*k) for k in range(8))
for o in (0,4,8,12,21):
    e = float((tot==u32(o)).mean())
    print(f'  sum(sides) == u32@{o}: {e:.4f}')
m = tot>0
print('  sum(sides)>0 rows', int(m.sum()), 'median', int(np.median(tot[m])))
print('  ratio sum/@0 median', float(np.median(tot[m]/np.maximum(1,u32(0)[m]))))
print('== per-slot 8th byte (level?) at 64+8k+7 ==')
for k in range(8):
    u,c = np.unique(ms[:,64+8*k+7], return_counts=True)
    print(f'  side{k} b7: ' + ', '.join(f'{int(a)}x{int(b)}' for a,b in zip(u[:6],c[:6])))
