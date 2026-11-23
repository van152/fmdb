import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _x7 import build_cands
import struct

raw=load('client',27)
print('len',len(raw),'hdr',raw[:14].hex(),'footer',raw[-8:].hex())
# show first 3 rows bytes with offsets
b=raw[14:141]
print('row0 len 127')
for i in range(0,len(b),16):
    print(f'  {i:4d}: {b[i:i+16].hex(" ")}  {b[i:i+16]!r}')
EOF_MARK=0
