import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw = core['load_payload']('server', 24)
rows = np.load('scratch/t76a/_rows24.npy')
n = len(rows)
len86 = np.array([l for _,l in rows]) == 86
idx86 = np.where(len86)[0]
print('86-byte rows:', len(idx86))
# build a matrix from the first 73 bytes (86-13 identity) of 86-byte rows
M = np.stack([np.frombuffer(raw, np.uint8, 73, int(rows[j][0])) for j in idx86])
print('M', M.shape)
for o in range(73):
    u = np.unique(M[:,o])
    s = f'{o:3d} d={len(u):3d}'
    if len(u)<=6: s += f' {u.tolist()}'
    if o+2 <= 73:
        v2 = np.ascontiguousarray(M[:,o:o+2]).view('<u2').ravel()
        s += f' u16d={len(np.unique(v2))}[{v2.min()},{v2.max()}]'
    if o+4 <= 73:
        v4 = np.ascontiguousarray(M[:,o:o+4]).view('<u4').ravel()
        s += f' u32d={len(np.unique(v4))}[{v4.min()},{v4.max()}] ff={int((v4==0xffffffff).sum())}'
    print(s)
