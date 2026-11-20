import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_c = core['load_payload']('client', 21); raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
mc = np.frombuffer(raw_c, np.uint8, H+n*38)[H:].reshape(n,38)
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
print('server[:,143:181] == client[:,:] :', np.array_equal(ms[:,143:181], mc))
print('per-row equality:', int((ms[:,143:181]==mc).all(axis=1).sum()), '/', n)
for co in range(25, 38):
    hits = [so for so in range(181) if np.array_equal(mc[:,co], ms[:,so]) and not (mc[:,co]==0).all()]
    print('client', co, '->', hits)
# direct u32 checks
def u32(m,o): return np.ascontiguousarray(m[:,o:o+4]).view('<u4').ravel()
print('client ord@25 == arange:', bool((u32(mc,25)==np.arange(n)).all()))
print('server ord@168 == arange:', bool((u32(ms,168)==np.arange(n)).all()))
print('server u32@172 == arange:', int((u32(ms,172)==np.arange(n)).sum()))
print('server u32@172 == server u32@176:', bool((u32(ms,172)==u32(ms,176)).all()))
print('client u32@29 == client u32@33:', bool((u32(mc,29)==u32(mc,33)).all()))
