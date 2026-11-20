import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21); raw_c = core['load_payload']('client', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
mc = np.frombuffer(raw_c, np.uint8, H+n*38)[H:].reshape(n,38)
def u32(o,m=ms): return np.ascontiguousarray(m[:,o:o+4]).view('<u4').ravel().astype(np.int64)
a0, a8 = u32(0), u32(8)
pred = a0 + a0//4
print('@8 == @0 + @0//4 :', float((a8==pred).mean()), ' where @8!=@0:', int((a8!=a0).sum()), 'agreement', float((a8[a8!=a0]==pred[a8!=a0]).mean()))
print('@8 == ceil:', float((a8==-(-a0*5//4)).mean()), ' floor:', float((a8==(a0*5)//4).mean()), ' trunc:', float((a8==pred).mean()))
print()
# @16 by Scti clustering
s16 = u32(16); m = s16 != 0xffffffff
scti = u32(3, mc)
vals, cnts = np.unique(s16[m], return_counts=True)
rep = vals[cnts>=2]
same = 0; tot = 0
for v in rep[:400]:
    idx = np.where(s16==v)[0]
    tot += 1
    if len(set(scti[idx].tolist())) == 1: same += 1
print(f'@16 repeated values (>=2) tested {tot}: same Scti in {same} ({same/max(1,tot):.3f})')
rng = np.random.default_rng(9)
csame=0
for _ in range(tot):
    idx = rng.integers(0, n, 2)
    if scti[idx[0]]==scti[idx[1]]: csame+=1
print('control random pairs same Scti:', csame/tot)
print()
print('@16 == @0..? none. Check @16 vs Scti of target row (nearby stadium?):')
print('  same Scti as referenced row:', float((scti[m]==scti[np.minimum(s16[m],n-1)]).mean()))
