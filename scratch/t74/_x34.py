import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct
raw=load('client',7)
p,b,_,_=dp_walk(raw,'c7',14,len(raw)-8,208)
rows=[(x[0],x[1]) for x in b]
for i in (29,40,42,16,20):
    s,e=rows[i]
    print(f'=== row{i} [{s},{e}) len={e-s}')
    body=raw[s:e]
    for j in range(0,len(body),16):
        print(f'  {j:4d} {body[j:j+16].hex(" ")}  {body[j:j+16]!r}')
