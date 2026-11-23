import sys, struct, importlib.util
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
spec=importlib.util.spec_from_file_location('t82','scripts/t82_extra3_remaining.py')
m82=importlib.util.module_from_spec(spec); spec.loader.exec_module(m82)
from pathlib import Path
res={}
for arch in ('server','client'):
    ent,raw=m82.open_fmf(Path('scratch/data/%s_db.dat'%arch))
    b=m82.extract_fmf_member(raw,ent,'%s_db/table_extra_9.dat'%arch)
    res[arch]=b
    print('==',arch,len(b))
    print(b[:64].hex())
    print('u16@6',struct.unpack_from('<H',b,6)[0],'u32@8',struct.unpack_from('<I',b,8)[0])
    # candidate: 12 hdr, then 251 rows fixed len
    for f in range(0,40):
        if (len(b)-12-f)%251==0: print('  fixed row len', (len(b)-12-f)//251, 'footer',f)
    # find u32 0..5 sequence from 12
    print('  first u32s', [struct.unpack_from('<I',b,12+4*i)[0] for i in range(8)])
