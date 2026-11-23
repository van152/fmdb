import sys, struct, importlib.util
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
spec=importlib.util.spec_from_file_location('t82','scripts/t82_extra3_remaining.py')
m82=importlib.util.module_from_spec(spec); spec.loader.exec_module(m82)
from pathlib import Path
for arch in ('server','client'):
    ent,raw=m82.open_fmf(Path('scratch/data/%s_db.dat'%arch))
    b=m82.extract_fmf_member(raw,ent,'%s_db/table_extra_9.dat'%arch)
    print('==',arch,len(b),'count@9',struct.unpack_from('<I',b,9)[0],'u32@13',struct.unpack_from('<I',b,13)[0])
    p=17; rows=[]
    for k in range(251):
        if p+4>len(b): break
        nl=struct.unpack_from('<I',b,p)[0]
        if nl>200 or p+4+nl>len(b): rows.append(('bad',k,p,nl)); break
        nm=b[p+4:p+4+nl].decode('utf-8','replace')
        rows.append((k,p,nl,nm))
        p+=4+nl
        # try to find next row: assume 45-ish? print hex
        if k<2: print('   after name at',p,b[p:p+50].hex())
        break
