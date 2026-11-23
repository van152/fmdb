import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

def rows_of(arch,tid,n):
    raw=load(arch,tid)
    p,b,_,_ = dp_walk(raw,f'{arch}{tid}',14,len(raw)-8,n)
    return raw, [(x[0],x[1]) for x in b]

raw,rows = rows_of('client',18,1567)
# midlen hist
midlens=collections.Counter()
for s,e in rows:
    nl1=struct.unpack_from('<I',raw,s)[0]
    p=s+4+nl1; nl2=struct.unpack_from('<I',raw,p)[0]; p+=4+nl2
    midlens[e-13-p]+=1
print('client midlens', sorted(midlens.items())[:20], 'distinct', len(midlens))
# check if nl1==nl2 always
print('nl1==nl2 all?', all(struct.unpack_from('<I',raw,s)[0]==struct.unpack_from('<I',raw,s+4+struct.unpack_from('<I',raw,s)[0])[0] for s,e in rows))
# t18 server midlens
raws,rowss = rows_of('server',18,1567)
midlens_s=collections.Counter()
for s,e in rowss:
    nl1=struct.unpack_from('<I',raws,s)[0]
    p=s+4+nl1; nl2=struct.unpack_from('<I',raws,p)[0]; p+=4+nl2
    midlens_s[e-13-p]+=1
print('server midlens', sorted(midlens_s.items())[:20], 'distinct', len(midlens_s))
EOF=0
