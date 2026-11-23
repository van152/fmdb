import runpy, sys, struct, collections
import numpy as np
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
def load(arch,tid,n,S):
    raw=dump['load_payload'](codec,arch,tid); H=len(raw)-n*S-8
    return raw, np.frombuffer(raw,dtype=np.uint8,count=n*S,offset=H).reshape(n,S)

raw,M=load('client',2,56293,43)
print('city @18 byte hist', collections.Counter(M[:,18].tolist()).most_common(10), 'distinct', len(set(M[:,18].tolist())))
i16=M[:,19:21].copy().view('<i2').ravel()
print('city i16@19 range', int(i16.min()), int(i16.max()), 'n outside[-1000,8000]', int(((i16< -1000)|(i16>8000)).sum()))
i16b=M[:,20:22].copy().view('<i2').ravel()
print('city i16@20 range', int(i16b.min()), int(i16b.max()))
u32=M[:,25:29].copy().view('<u4').ravel()
print('city @25 max excl sentinel', int(u32[u32!=0xffffffff].max()), 'sentinel', int((u32==0xffffffff).sum()))
u32_21=M[:,21:25].copy().view('<u4').ravel()
print('city @21 max excl sentinel', int(u32_21[u32_21!=0xffffffff].max()), 'sentinel', int((u32_21==0xffffffff).sum()))
print('city byte29 hist', collections.Counter(M[:,29].tolist()).most_common(6))

print('\n--- region client 32B business, u32 grid @ offsets')
rc,Mc=load('client',19,28,45); rs,Ms=load('server',19,28,46)
for o in range(0,33):
    c=Mc[:,o]
    u=np.unique(c)
    print(f' c[{o:02d}] distinct={len(u):2d} min={int(c.min()):3d} max={int(c.max()):3d} vals={sorted(set(u.tolist()))[:8]}')
