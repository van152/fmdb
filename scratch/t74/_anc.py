import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections
for arch in ('client','server'):
    raw=load(arch,7)
    _,b,_,_=dp_walk(raw,f'{arch}7',14,len(raw)-8,208)
    rows=[(x[0],x[1]) for x in b]
    ok3=0;ok7=0;s3=collections.Counter()
    for i,(s,e) in enumerate(rows):
        r3,d7=struct.unpack_from('<II',raw,s+3)
        if r3==i: ok3+=1
        if d7==i: ok7+=1
        s3[(r3 if r3<300 else 'big')]+=1
    print(arch,'u32@row+3==idx:',ok3,'/208   u32@row+7==idx:',ok7)
    print('   u32@+3 value dist',s3.most_common(5))
    # what is at row+3 semantically: bytes 3..7 of name_len high byte + first char
    print('   row0 bytes0..12',raw[14:27].hex(' '))
