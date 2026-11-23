import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
def u32(o): return np.ascontiguousarray(ms[:, o:o+4]).view('<u4').ravel().astype(np.int64)
own = u32(16)
null = own == 0xffffffff
print('== Soty(@20) x Sowi-null cross-tab ==')
import collections
tab = collections.Counter(zip(ms[:,20].tolist(), null.tolist()))
for (b, isnull), c in sorted(tab.items()):
    print(f'  @20={b:3d} sowi_null={isnull} n={c}')
print()
print('== byte34 hist x Sowi-null (Soty enum 1..5) ==')
tab = collections.Counter(zip(ms[:,34].tolist(), null.tolist()))
for (b, isnull), c in sorted(tab.items()):
    print(f'  @34={b} sowi_null={isnull} n={c}')
print()
print('== byte33 hist (Spty enum 1..8) x @34 ==')
tab = collections.Counter(zip(ms[:,33].tolist(), ms[:,34].tolist()))
for (a,b), c in sorted(tab.items())[:20]:
    print(f'  @33={a} @34={b} n={c}')
