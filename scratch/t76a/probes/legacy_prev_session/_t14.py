import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy'); n = len(rows)
starts = rows[:,0].astype(np.int64); lens = rows[:,1].astype(np.int64)
A = np.frombuffer(raw, np.uint8)
def c32(o):
    return (A[starts+o].astype(np.uint64) | (A[starts+o+1].astype(np.uint64)<<8)
            | (A[starts+o+2].astype(np.uint64)<<16) | (A[starts+o+3].astype(np.uint64)<<24))
uids = np.load('scratch/t76a/_uids24.npy').astype(np.uint64)
u21 = set(np.load('scratch/t76a/_uids21.npy').tolist())
u2 = set(np.load('scratch/t76a/_uids2.npy').tolist())
u3 = set(np.load('scratch/t76a/_uids3.npy').tolist())
print('== FK lane scan: whole u32 == reference UID set, rate 1.0 ==')
print('off  fill  t21      t2       t3')
for o in range(0, 70):
    ok = (o+4 <= lens-13)
    if ok.mean() < 0.99: continue
    v = c32(o)
    h21 = float(np.isin(v, list(u21)).mean()); h2 = float(np.isin(v, list(u2)).mean()); h3 = float(np.isin(v, list(u3)).mean())
    if max(h21,h2,h3) > 0.3:
        print(f'{o:3d} {ok.mean():.3f} {h21:.4f} {h2:.4f} {h3:.4f}')
