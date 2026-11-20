import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21); raw_c = core['load_payload']('client', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
mc = np.frombuffer(raw_c, np.uint8, H+n*38)[H:].reshape(n,38)
# exact column equality client off -> server offs
for co in range(38):
    hits = [so for so in range(181) if np.array_equal(mc[:,co], ms[:,so]) and not (mc[:,co]==0).all()]
    if hits:
        print(f'client off {co:2d} == server offs {hits}')
