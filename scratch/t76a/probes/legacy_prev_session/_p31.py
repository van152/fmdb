import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
pre = ms[:, :143]
# print const map as compact picture for a sample row with offsets
def dump(j, lo=0, hi=143):
    r = ms[j]
    print('row', j)
    for k in range(lo, hi, 8):
        chunk = r[k:min(k+8,hi)]
        print(f'  {k:3d}: ' + ' '.join(f'{b:02x}' for b in chunk) +
              '   ' + ''.join(f'{b:3d} ' for b in chunk))
for j in (8838, 0, 71):
    dump(j)
    print()
