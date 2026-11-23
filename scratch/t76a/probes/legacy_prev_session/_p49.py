import runpy, sys, struct
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21); raw_c = core['load_payload']('client', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
mc = np.frombuffer(raw_c, np.uint8, H+n*38)[H:].reshape(n,38)
def u32(o,m=ms): return np.ascontiguousarray(m[:,o:o+4]).view('<u4').ravel().astype(np.int64)
a0,a8,a12,a21 = u32(0),u32(8),u32(12),u32(21)
print('@21==@0', float((a21==a0).mean()), '@21==@12', float((a21==a12).mean()))
print('@21 zero', int((a21==0).sum()))
print('when @21!=0: @21==@0', float((a21[a21>0]==a0[a21>0]).mean()))
print()
print('== client byte bits ==')
for o in (0,1,11):
    col = mc[:,o]
    bits = [(col>>b)&1 for b in range(8)]
    print(f' byte{o}: set-rates ' + ' '.join(f'b{b}={float(x.mean()):.3f}' for b,x in enumerate(bits)))
print()
print('== client byte11 value counts detail ==')
u,c = np.unique(mc[:,11], return_counts=True)
for a,b in zip(u,c): print(f'   {a:4d} (0x{a:02x}) n={b}')
print()
print('== server @20 const? ==', int(np.unique(ms[:,20]).size), np.unique(ms[:,20]))
print('== client @2,@5,@6,@12,@14 const ==', {o: int(mc[0,o]) for o in (2,5,6,12,14)})
