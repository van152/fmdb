import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct

raw=load('client',7)
rows=[(14,204),(204,395),(395,632)]
for i,(s,e) in enumerate(rows):
    body=raw[s:e]
    print('row',i,'len',len(body))
    print(' ',body.hex())
    print(' ',body)
