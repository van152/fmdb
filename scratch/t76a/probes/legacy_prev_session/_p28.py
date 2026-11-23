import runpy, sys
import numpy as np
sys.path.insert(0,'scripts')
core = runpy.run_path('scripts/t73_mapper_core.py', run_name='core')
raw_s = core['load_payload']('server', 21)
H, n = 14, 48413
ms = np.frombuffer(raw_s, np.uint8, H+n*181)[H:].reshape(n,181)
def u32(o): return np.ascontiguousarray(ms[:, o:o+4]).view('<u4').ravel()
lat = np.ascontiguousarray(ms[:, 160:164]).view('<f4').ravel()
lon = np.ascontiguousarray(ms[:, 164:168]).view('<f4').ravel()
def show(name, la, lo, r=0.02):
    m = (np.abs(lat-la)<r) & (np.abs(lon-lo)<r)
    idx = np.where(m)[0]
    print(f'{name}: {len(idx)} rows near ({la},{lo})')
    for j in idx[:6]:
        print('   row', j, 'lat %.5f lon %.5f' % (lat[j], lon[j]),
              {o: int(u32(o)[j]) for o in (0,4,8,12,16,21)})
show('Wembley', 51.5560, -0.2796)
show('Camp Nou', 41.3809, 2.1228)
show('San Siro', 45.4781, 9.1240)
show('Santiago Bernabeu', 40.4531, -3.6883)
show('Old Trafford', 53.4631, -2.2913)
show('Maracana', -22.9121, -43.2302)
