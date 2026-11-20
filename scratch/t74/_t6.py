import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct, collections

raw=load('client',6)
n=len(raw); print('t6 client payload',n,'count u32@8',struct.unpack_from('<I',raw,8)[0])
print('head',raw[:40].hex(' '))
# try fixed stride
c=struct.unpack_from('<I',raw,8)[0]
for stride in (random for random in []): pass
for st in range(8,80):
    if 14+c*st+8==n: print('fixed stride candidate',st)
print('tail',raw[-24:].hex(' '))
