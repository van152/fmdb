import os,runpy,pathlib,sys,json,struct
os.environ.setdefault('FM24_DB_DIR','D:/tmp2b/fm24-db/scratch/data')
ROOT=pathlib.Path('D:/tmp2b/fm24-db')
c=runpy.run_path(str(ROOT/'scripts/t74_row_frames9.py'))
k=runpy.run_path(str(c['READER_VERIFY'])); C=runpy.run_path(str(k['OLD_READER_PATH']))
for tid,name in ((25,'comp'),(24,'team'),(10,'nation')):
    try:
        b=c['payload'](C,'server',tid); print(name,tid,'len',len(b),'n@8',struct.unpack_from('<I',b,8)[0])
        open(ROOT/f'scratch/t88/t{tid}.bin','wb').write(b)
    except Exception as e: print(name,'ERR',e)
