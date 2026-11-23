import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct

raw=load('client',7)
p,b,_,_=dp_walk(raw,'c7',14,len(raw)-8,208)
rows=[(x[0],x[1]) for x in b]
for i in (0,6,7,10):
    s,e=rows[i]
    nl=struct.unpack_from('<I',raw,s)[0]
    print(f'=== row{i} [{s},{e}) len={e-s} name_len={nl}')
    body=raw[s:e]
    p0=s+4+nl
    print('  6B pre',raw[p0:p0+6].hex(),'urlLen',struct.unpack_from('<I',raw,p0+6)[0])
    mid=raw[p0+6+4+struct.unpack_from('<I',raw,p0+6)[0]: e-13]
    print('  mid len',len(mid))
    for j in range(0,len(mid),16):
        print(f'    {j:4d} {mid[j:j+16].hex(" ")}  {mid[j:j+16]!r}')
