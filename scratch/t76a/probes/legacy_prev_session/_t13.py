import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy'); n = len(rows)
starts = rows[:,0].astype(np.int64); lens = rows[:,1].astype(np.int64)
A = np.frombuffer(raw, np.uint8)
def col32(o):
    return (A[starts+o].astype(np.uint32) | (A[starts+o+1].astype(np.uint32)<<8)
            | (A[starts+o+2].astype(np.uint32)<<16) | (A[starts+o+3].astype(np.uint32)<<24))
def col16(o):
    return (A[starts+o].astype(np.uint32) | (A[starts+o+1].astype(np.uint32)<<8))
print('== pairwise u32 equality over ALL rows (offsets 0..24) ==')
offs = list(range(0, 25, 2))
for a in offs:
    for b in offs:
        if b<=a: continue
        if np.array_equal(col32(a), col32(b)):
            print(f'  u32@{a} == u32@{b}  ALL ROWS')
print()
print('== u16 equality ==')
for a in offs:
    for b in offs:
        if b<=a: continue
        if np.array_equal(col16(a), col16(b)):
            print(f'  u16@{a} == u16@{b}  ALL ROWS')
print()
print('== date-pair hypothesis scan over ALL rows (year in 1900 or 1850..2035, doy 0..366) ==')
for d_o in range(0, 30, 2):
    for y_o in range(0, 30, 2):
        if y_o == d_o: continue
        d, y = col16(d_o), col16(y_o)
        leap = ((y%4==0)&(y%100!=0))|(y%400==0)
        mx = np.where(leap, 366, 365)
        ok = ((d>=1)&(d<=mx)&(((y>=1850)&(y<=2035))|(y==0)))
        r = ok.mean()
        if r > 0.97:
            print(f'  doy@{d_o} year@{y_o}: {r:.4f} (y==0: {int((y==0).sum())}, y==1900: {int((y==1900).sum())})')
