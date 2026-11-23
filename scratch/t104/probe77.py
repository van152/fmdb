import sys, struct, importlib.util
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
spec=importlib.util.spec_from_file_location('t82','scripts/t82_extra3_remaining.py')
m82=importlib.util.module_from_spec(spec); spec.loader.exec_module(m82)
from pathlib import Path
ent,raw=m82.open_fmf(Path('scratch/data/server_db.dat'))
b=m82.extract_fmf_member(raw,ent,'server_db/table_extra_9.dat')
p=12
for k in range(3):
    o,nl=struct.unpack_from('<II',b,p)
    nm=b[p+8:p+8+nl].decode('utf-8')
    print('row',k,'ord',o,'name',repr(nm))
    print('   after name:', b[p+8+nl:p+8+nl+48].hex())
    p+=8+nl
    print('   next bytes:', b[p:p+40].hex())
    p+=40
