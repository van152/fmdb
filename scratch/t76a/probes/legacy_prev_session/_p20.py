import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
pre = ms[:, :143]
L = 143
best = []
for p in range(1, 60):
    eq = [o for o in range(L-p) if np.array_equal(pre[:,o], pre[:,o+p])]
    if len(eq) >= 3:
        best.append((p, len(eq), eq[:20]))
for p, c, ex in sorted(best, key=lambda t: -t[1])[:14]:
    print(f'period {p:2d}: identical column pairs={c:3d} ex {ex}')
print()
# also: which offsets are constant, and value
consts = [(o, int(pre[0,o])) for o in range(L) if (pre[:,o]==pre[0,o]).all()]
print('constant offsets count', len(consts))
print(consts)
