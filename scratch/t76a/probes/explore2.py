import runpy, sys
import numpy as np
sys.path.insert(0, 'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_c = core['load_payload']('client', 21)
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
mc = np.frombuffer(raw_c, np.uint8, H + n * 38)[H:].reshape(n, 38)
ms = np.frombuffer(raw_s, np.uint8, H + n * 181)[H:].reshape(n, 181)
print('server[143:181]==client[0:38]:', np.array_equal(ms[:, 143:181], mc))
print('rows all equal:', int((ms[:, 143:181] == mc).all(axis=1).sum()), '/', n)
print('\nrow0 client', mc[0].tolist())
print('row0 server[0:60]', ms[0, :60].tolist())
print('row1 client', mc[1].tolist())
print('row2 client', mc[2].tolist())
print('row0 server[60:143]', ms[0, 60:143].tolist())
print('\nclient byte distinct counts:')
for o in range(25):
    u = np.unique(mc[:, o])
    print(f'  b{o:2d} d={u.size:4d}', u[:14].tolist() if u.size <= 14 else f'min={u.min()} max={u.max()}')
print('\nclient u16@0 distinct:', np.unique(np.ascontiguousarray(mc[:, 0:2]).view('<u2').ravel())[:20].tolist())
