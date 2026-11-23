import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
raw=load('server',24)
for base in (5951953, 5966946, 5974623, 8818821):
    print('=== base',base)
    seg=raw[base-40:base+120]
    for j in range(0,len(seg),16):
        off=base-40+j
        print(f'  {off:8d} {seg[j:j+16].hex(" ")}  {seg[j:j+16]!r}')
