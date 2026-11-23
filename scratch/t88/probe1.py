import os,runpy,pathlib,hashlib,json,struct
os.environ.setdefault('FM24_DB_DIR','D:/tmp2b/fm24-db/scratch/data')
ROOT=pathlib.Path('D:/tmp2b/fm24-db')
c=runpy.run_path(str(ROOT/'scripts/t74_row_frames9.py'))
k=runpy.run_path(str(c['READER_VERIFY']))
C=runpy.run_path(str(k['OLD_READER_PATH']))
for side in ('client','server'):
    fn=f'{side}_db.dat'; p=c['db_dir']()/fn
    ents=C['list_tables'](p,fn)
    print(side,len(ents),json.dumps(ents[0],ensure_ascii=False)[:300])
    print(' 45:',[e for e in ents if e.get('table_id') in (45,'45')][:2])
