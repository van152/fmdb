import os,runpy,pathlib,hashlib,json,struct
import numpy as np
os.environ.setdefault('FM24_DB_DIR','D:/tmp2b/fm24-db/scratch/data')
ROOT=pathlib.Path('D:/tmp2b/fm24-db')
c=runpy.run_path(str(ROOT/'scripts/t74_row_frames9.py'))
k=runpy.run_path(str(c['READER_VERIFY'])); C=runpy.run_path(str(k['OLD_READER_PATH']))
b=c['payload'](C,'server',45)
open(ROOT/'scratch/t88/t45.bin','wb').write(b)
print('len',len(b))
print('head',b[:40].hex())
print('tail',b[-60:].hex())
n=struct.unpack_from('<I',b,8)[0]; print('n@8',n, 'u32@12',struct.unpack_from('<I',b,12)[0])
bb=np.frombuffer(b,np.uint8)
# marker-zero positions
z=np.flatnonzero(bb==0)
print('zero count',len(z))
# tail structure: look at last 13B groups
t=b[-13:]
print('last13',t.hex(),'ord,uid,uid,mk',struct.unpack_from('<II',t,0),t[12])
