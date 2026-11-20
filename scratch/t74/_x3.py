import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct

raw=load('client',7)
def dumprow(s,e,name=''):
    b=raw[s:e]
    print(f'--- row [{s},{e}) len={len(b)} {name}')
    for i in range(0,len(b),8):
        c=b[i:i+8]
        print(f'   +{i:4d} {c.hex(" "):<24} {"".join(chr(x) if 32<=x<127 else "." for x in c)}')
dumprow(14,204,'Daily Mirror')
