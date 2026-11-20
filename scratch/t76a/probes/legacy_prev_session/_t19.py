import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy'); n=len(rows)
starts = rows[:,0].astype(np.int64); lens = rows[:,1].astype(np.int64)
A = np.frombuffer(raw, np.uint8)
M = np.stack([A[starts[j]:starts[j]+73] for j in range(n)])
print('all-row matrix', M.shape)
print('off  d      min  max   ff      z    | 86-only d')
idx86 = np.where(lens==86)[0]
for o in range(73):
    c = M[:,o]; u=len(np.unique(c))
    d86 = len(np.unique(M[idx86,o]))
    print(f'{o:3d} {u:6d} {c.min():4d} {c.max():4d} {int((c==255).sum()):6d} {int((c==0).sum()):6d} | {d86:6d}')
