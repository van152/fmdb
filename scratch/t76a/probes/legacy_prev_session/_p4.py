import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_c = core['load_payload']('client', 21)
raw_s = core['load_payload']('server', 21)
H, n, Sc, Ss = 14, 48413, 38, 181
mc = np.frombuffer(raw_c, dtype=np.uint8, count=H+n*Sc)[H:].reshape(n, Sc)
ms = np.frombuffer(raw_s, dtype=np.uint8, count=H+n*Ss)[H:].reshape(n, Ss)
# does server tail 143:181 equal client 0:38 ?
eq = (ms[:, 143:181] == mc[:, 0:38]).all(axis=1)
print('server[143:181]==client[0:38] rows:', int(eq.sum()), '/', n)
# which rows differ and how
bad = np.where(~eq)[0][:10]
print('first bad rows', bad)
for j in bad[:3]:
    print(j, mc[j].hex(' '), '|', ms[j,143:181].hex(' '))
# offsets 0..24 of client, u8 distinct / u32 stats precisely
for off in range(0, 25):
    col = mc[:, off]
    print(off, 'u8uniq', len(np.unique(col)), 'min/max', col.min(), col.max())
# check u32 at 3
for off in (0,1,3,4):
    v = mc[:, off:off+4].copy().view('<u4').ravel()
    print('u32@',off, v.min(), v.max(), len(np.unique(v)))
v2 = mc[:, 4:6].copy().view('<u2').ravel()
print('u16@4', v2.min(), v2.max(), len(np.unique(v2)))
print('rows where u16@4>0:', int((v2>0).sum()), 'sample', np.unique(v2)[:10])
