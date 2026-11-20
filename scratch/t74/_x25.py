import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

def rows_of(arch,tid,n):
    raw=load(arch,tid)
    p,b,_,_ = dp_walk(raw,f'{arch}{tid}',14,len(raw)-8,n)
    return raw, [(x[0],x[1]) for x in b]

raw,rows = rows_of('client',18,1567)
# find rows with midlen != 44
big=[]
for i,(s,e) in enumerate(rows):
    nl1=struct.unpack_from('<I',raw,s)[0]
    p=s+4+nl1; nl2=struct.unpack_from('<I',raw,p)[0]; p+=4+nl2
    ml=e-13-p
    if ml!=44: big.append((i,s,e,ml,nl1,nl2))
print('n variable rows',len(big))
for i,s,e,ml,nl1,nl2 in big[:6]:
    print(f'=== row{i} len={e-s} midlen={ml} nl=({nl1},{nl2})')
    body=raw[s:e]
    for j in range(0,len(body),16):
        print(f'  {j:4d} {body[j:j+16].hex(" ")}  {body[j:j+16]!r}')
