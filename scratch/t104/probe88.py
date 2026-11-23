import sys, struct, importlib.util
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
spec=importlib.util.spec_from_file_location('t82','scripts/t82_extra3_remaining.py')
m82=importlib.util.module_from_spec(spec); spec.loader.exec_module(m82)
from pathlib import Path
ent,raw=m82.open_fmf(Path('scratch/data/server_db.dat'))
b=m82.extract_fmf_member(raw,ent,'server_db/table_extra_9.dat')
r=b[12:153]
print('row0 len',len(r))
for o in range(0,len(r)):
    print('%3d:%02x'%(o,r[o]), end=' ')
    if o%10==9: print()
print()
print(repr(r))
