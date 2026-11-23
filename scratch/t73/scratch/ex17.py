import runpy, sys, struct
import numpy as np
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()

def load(arch,tid,n,S):
    raw=dump['load_payload'](codec,arch,tid)
    H=len(raw)-n*S-8
    return raw, np.frombuffer(raw,dtype=np.uint8,count=n*S,offset=H).reshape(n,S)

raw,M=load('client',2,56293,43)
print('city 43 bytes, col distinct & top values')
for o in range(43):
    c=M[:,o]
    u=np.unique(c)
    print(f' {o:02d}: n_u={len(u):3d} min={c.min():3d} max={c.max():3d} mode={u[np.argmax(np.bincount(c))]:3d} ',
          ('ALLZERO' if len(u)==1 and u[0]==0 else ''))
# u32 candidate windows across whole 30-byte business area at each shift
print('\n city u32 windows (looking for ordered / f32-valid)')
for o in range(0,43-3):
    v=M[:,o:o+4].copy().view('<u4').ravel()
    inc = np.all(v[1:]>=v[:-1])
    f=[np.frombuffer(M[i,o:o+4].tobytes(),dtype='<f4')[0] for i in range(len(M))]
    good=sum(1 for x in f if -90<=x<=90)
    print(f'  @{o:02d} u32 min={v.min()} max={v.max()} strictly_inc={inc} f32_in_-90..90={good}/{len(M)}')
