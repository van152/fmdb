import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

raw=load('client',27)
p,b,_,_=dp_walk(raw,'c27',14,len(raw)-8,334)
print('rows',len(b))
for i in (0,1,2,3,4,5,333):
    s,e,u=b[i]
    print(f'--- row {i} [{s},{e}) len={e-s} u={u}')
    body=raw[s:e]
    print('   ', body[:8].hex(' '), '...', body[-20:].hex(' '))
# hypothesis: len(u32) at s+off0, name, then rest
for i in range(8):
    s,e,u=b[i]
    for off in range(0,8):
        nl=struct.unpack_from('<I',raw,s+off)[0]
        if 3<=nl<=60 and s+off+4+nl<=e:
            nm=raw[s+off+4:s+off+4+nl]
            try:
                txt=nm.decode('utf-8')
            except Exception:
                continue
            if all(31<ord(c)<128 for c in txt):
                print(f'row{i} off={off} nl={nl} name={txt!r} rest_after_name={e-(s+off+4+nl)}')
