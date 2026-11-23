import sys, struct, runpy, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
import importlib.util
spec=importlib.util.spec_from_file_location('t82','scripts/t82_extra3_remaining.py')
m82=importlib.util.module_from_spec(spec); spec.loader.exec_module(m82)
from pathlib import Path
for arch in ('server','client'):
    p=Path('scratch/data/%s_db.dat'%arch)
    ent,raw=m82.open_fmf(p)
    ks=[k for k in ent if 'extra' in k]
    print(arch, len(ent), 'extra keys', ks[:10])
    for k in ('%s_db/table_extra_3.dat'%arch,'%s_db/table_extra_9.dat'%arch,'%s_db/table_extra_24.dat'%arch):
        if k in ent:
            b=m82.extract_fmf_member(raw,ent,k)
            print('  ',k,'len',len(b),'head',b[:16].hex(),'count',struct.unpack_from('<I',b,8)[0],'ver',struct.unpack_from('<H',b,6)[0])
