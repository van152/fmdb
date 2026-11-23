import sys, struct, importlib.util, collections
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
spec=importlib.util.spec_from_file_location('t82','scripts/t82_extra3_remaining.py')
m82=importlib.util.module_from_spec(spec); spec.loader.exec_module(m82)
from pathlib import Path
ent,raw=m82.open_fmf(Path('scratch/data/server_db.dat'))
b=m82.extract_fmf_member(raw,ent,'server_db/table_extra_9.dat')
for off in (12,153,348,867,1299):
    print(off, b[off:off+24].hex(), struct.unpack_from('<I',b,off)[0])
# candidate starts from t50: 12,348,867
starts=[12,348,867]
for i,s in enumerate(starts):
    print('row',i,'at',s,'len', (starts[i+1]-s) if i+1<len(starts) else None)
# verify extra_24 fixed 82
e24=m82.extract_fmf_member(raw,ent,'server_db/table_extra_24.dat')
print('extra24 len',len(e24),'12+84507*82 =',12+84507*82)
for k in range(5):
    r=e24[12+82*k:12+82*(k+1)]
    print(k, r.hex())
