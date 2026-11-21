import os,runpy,pathlib,struct,json
import numpy as np
os.environ.setdefault('FM24_DB_DIR','D:/tmp2b/fm24-db/scratch/data')
ROOT=pathlib.Path('D:/tmp2b/fm24-db')
c=runpy.run_path(str(ROOT/'scripts/t74_row_frames9.py'))
k=runpy.run_path(str(c['READER_VERIFY'])); C=runpy.run_path(str(k['OLD_READER_PATH']))
for tid in (3,):
    b=c['payload'](C,'server',tid); print('t%d len'%tid,len(b))
    open(ROOT/f'scratch/t88/t{tid}.bin','wb').write(b)
    print(' head',b[:32].hex(' '))
    print(' tail',b[-32:].hex(' '))
