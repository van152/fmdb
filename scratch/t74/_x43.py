import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct

raw=load('client',27)
H,F=14,len(raw)-8
p,b,_,_=dp_walk(raw,'c27',H,F,334)
rows=[(x[0],x[1]) for x in b]

def idt(s,e):
    o,u1,u2,m=struct.unpack_from('<IIII',raw,e-13) if e-13+16<=len(raw) else (None,)*4
    return o,u1,u2,m
for i in (0,1,2):
    s,e=rows[i]
    print(f'row{i} [{s},{e}) len={e-s}')
    print('   last13',raw[e-13:e].hex(),'-> ord,uid,uid,mk',idt(s,e))
# alternative: boundary 141
print()
for cand in [(14,141),(141,267)]:
    s,e=cand
    o,u1,u2,m=struct.unpack_from('<II',raw,e-13)+struct.unpack_from('<I',raw,e-5)+ (raw[e-1],)
    print(cand,'len',e-s,'last13',raw[e-13:e].hex(),o,u1,u2,m)
