import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections
raw=load('client',47)
print('payload',len(raw),'count@8',struct.unpack_from('<I',raw,8)[0])
print('head 0..40',raw[:40].hex(' '))
for lo in (14,25):
    p,b,_,_=dp_walk(raw,f'c{lo}',lo,len(raw)-8,2488)
    lens=[x[1]-x[0] for x in b]
    print('lo',lo,'paths',p,'closure',b[-1][1]==len(raw)-8,'lens',min(lens),max(lens),
          'mod5',dict(collections.Counter((L-41)%5 for L in lens)),'sum',lo+sum(lens)+8==len(raw))
