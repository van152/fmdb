import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
def u32(o): return np.ascontiguousarray(ms[:, o:o+4]).view('<u4').ravel().astype(np.int64)
a0, a8 = u32(0), u32(8)
pred = np.ceil(a0*1.25).astype(np.int64)
print('@8 == ceil(@0*1.25):', float((a8==pred).mean()))
print('@8 == ceil(@0*1.25) among @8>@0:', float((a8[a8>a0]==pred[a8>a0]).mean()), 'n', int((a8>a0).sum()))
print('@8 == @0:', int((a8==a0).sum()))
print('@8 > @0:', int((a8>a0).sum()), '@8 < @0:', int((a8<a0).sum()))
bad = np.where((a8!=pred)&(a8!=a0))[0]
print('neither pred nor equal:', len(bad), 'sample', [(int(j), int(a0[j]), int(a8[j]), int(pred[j])) for j in bad[:6]])
print()
# @7 UID control
raw_c = core['load_payload']('client', 21)
mc = np.frombuffer(raw_c, np.uint8, H+n*38)[H:].reshape(n,38)
s7 = np.ascontiguousarray(mc[:,7:11]).view('<u4').ravel().astype(np.int64)
uid = np.ascontiguousarray(mc[:,29:33]).view('<u4').ravel().astype(np.int64)
m = s7 != 0xffffffff
print('@7 nonnull', int(m.sum()), 'in UID set:', float(np.isin(s7[m], set(uid.tolist())).mean()), 'in ordinal range:', float((s7[m]<n).mean()))
print('@7 == own ordinal:', int((s7==np.arange(n)).sum()), '@7 == own+1:', int((s7==np.arange(n)+1).sum()))
# do referenced rows share city?
scti = u32(3, mc) if False else np.ascontiguousarray(mc[:,3:7]).view('<u4').ravel().astype(np.int64)
print('same Scti as target:', float((scti[m]==scti[s7[m]]).mean()))
