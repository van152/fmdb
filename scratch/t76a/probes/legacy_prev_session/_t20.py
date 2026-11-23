import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy'); n=len(rows)
starts = rows[:,0].astype(np.int64); lens = rows[:,1].astype(np.int64)
A = np.frombuffer(raw, np.uint8)
def c32(o):
    return (A[starts+o].astype(np.uint64) | (A[starts+o+1].astype(np.uint64)<<8)
            | (A[starts+o+2].astype(np.uint64)<<16) | (A[starts+o+3].astype(np.uint64)<<24))
u21=set(np.load('scratch/t76a/_uids21.npy').tolist()); u2=set(np.load('scratch/t76a/_uids2.npy').tolist()); u3=set(np.load('scratch/t76a/_uids3.npy').tolist())
print('off fill null_ff null0 | t21 t2 t3  (rates among in-domain values)')
for o in range(0, 30):
    v = c32(o)
    ff = int((v==0xffffffff).sum()); z = int((v==0).sum())
    keep = (v!=0xffffffff)&(v!=0)
    if keep.sum() < 100: continue
    vv = v[keep].tolist()
    def r(s): return sum(1 for x in vv if x in s)/len(vv)
    print(f'{o:3d} {keep.mean():.3f} {ff:6d} {z:6d} | {r(u21):.4f} {r(u2):.4f} {r(u3):.4f}  n={len(vv)}')
