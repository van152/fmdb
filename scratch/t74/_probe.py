import runpy, pathlib, sys, struct
k=runpy.run_path('scratch/t01/inbox/t01k/verify.py')
codec=runpy.run_path(str(k['OLD_READER_PATH']))
m=runpy.run_path('scripts/fm24_dump.py')
import os
os.environ.setdefault('FM24_DB_DIR','D:/tmp2b/fm24-db/scratch/data')
def load(a,t): return m['load_payload'](codec,a,t)
