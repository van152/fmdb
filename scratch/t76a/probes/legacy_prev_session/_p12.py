import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n, Ss = 14, 48413, 181
ms = np.frombuffer(raw_s, np.uint8, H+n*Ss)[H:].reshape(n, Ss)
for j in (0,1,2,3,4):
    r = ms[j].tobytes()
    print('row',j)
    for k in range(0, 148, 4):
        print('  %3d: %s' % (k, r[k:k+4].hex(' ')))
