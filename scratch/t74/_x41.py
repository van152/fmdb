import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, difflib

raw=load('client',27)
p,b,_,_=dp_walk(raw,'c27',14,len(raw)-8,334)
rows=[(x[0],x[1]) for x in b]

def parts(i):
    s,e=rows[i]
    nl=struct.unpack_from('<I',raw,s)[0]
    nm=raw[s+4:s+4+nl]
    return s,e,nl,nm,raw[s+4+nl:e-13]

for i in (0,1,2,3):
    s,e,nl,nm,mid=parts(i)
    print(f'row{i} len={e-s} nl={nl} name={nm!r} midlen={len(mid)}')
    print('   mid',mid.hex(' '))

a=parts(0)[4]; c=parts(2)[4]
sm=difflib.SequenceMatcher(None,a,c,autojunk=False)
print('--- diff row0 vs row2 mid')
for tag,i1,i2,j1,j2 in sm.get_opcodes():
    if tag!='equal': print(tag,i1,i2,a[i1:i2].hex(),'|',j1,j2,c[j1:j2].hex())
