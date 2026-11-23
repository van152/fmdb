import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import numpy as np, struct, bisect

raw=load('server',24); n=len(raw)
fpos=np.load('scratch/t74/_fpos24.npy').tolist()
starts=[14]+[p+13 for p in fpos[:-1]]
rows=[(starts[i],fpos[i]+13) for i in range(len(fpos))]
for i in (0,1,2):
    s,e=rows[i]
    print(f'=== row{i} [{s},{e}) len={e-s} trailer_start={fpos[i]}')
    b=raw[s:e]
    for j in range(0,len(b),16):
        print(f'  {j:4d} {b[j:j+16].hex(" ")}  {b[j:j+16]!r}')
