import runpy, sys, struct, collections
import numpy as np
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
def load(arch,tid,n,S):
    raw=dump['load_payload'](codec,arch,tid); H=len(raw)-n*S-8
    return raw, np.frombuffer(raw,dtype=np.uint8,count=n*S,offset=H).reshape(n,S)
raw,M=load('client',2,56293,43)
for o in range(43):
    c=M[:,o]; u,cnt=np.unique(c,return_counts=True)
    print(f' {o:02d}: distinct={len(u):3d} min={c.min():3d} max={c.max():3d} mode={u[cnt.argmax()]:3d}({cnt.max()})', 'ALLZERO' if len(u)==1 and u[0]==0 else '')
print()
for o in range(0,40):
    v=M[:,o:o+4].copy().view('<u4').ravel()
    f=np.frombuffer(M[:,o:o+4].copy().tobytes(),dtype='<f4')
    print(f'  u32@{o:02d} min={v.min():<11} max={v.max():<11} inc={int(np.all(v[1:]>=v[:-1]))} f32good={int(sum(1 for x in f if -180<=x<=180))}/{len(M)}')
