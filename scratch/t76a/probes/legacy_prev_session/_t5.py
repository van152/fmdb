import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy')
n = len(rows)
u21 = np.load('scratch/t76a/_uids21.npy'); s21 = set(u21.tolist())
u2 = np.load('scratch/t76a/_uids2.npy'); s2 = set(u2.tolist())
u23 = np.load('scratch/t76a/_uids23.npy') if False else None
# stride-8 body: first 73 B is the fixed part for len-86 rows; but for var rows the tail differs.
# Strategy: for each offset o in 0..(min_len-13), read u32 over ALL rows where o+4 <= len-13
lens = rows[:,1]; starts = rows[:,0]
minlen = 13
maxbody = int(lens.min()) - 13
print('min row len', lens.min(), 'maxbody', maxbody)
print('col | fillrate | t21hit | t2hit | in-range-n(84507)')
for o in range(0, 74, 1):
    vals=[]; 
    for (s,l) in rows:
        if o+4 <= l-13:
            vals.append(struct.unpack_from('<I', raw, int(s+o))[0])
        else:
            vals.append(None)
    vals = [v for v in vals if v is not None]
    if len(vals) < n*0.5: continue
    arr = np.array(vals, dtype=np.int64)
    h21 = float(np.isin(arr, list(s21)).mean())
    h2 = float(np.isin(arr, list(s2)).mean())
    print(f'{o:4d} {len(vals)/n:.3f} {h21:.4f} {h2:.4f} {float((arr<n).mean()):.4f}')
