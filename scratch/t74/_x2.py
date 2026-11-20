import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct

def show(arch,tid,ranges,label):
    raw=load(arch,tid)
    print(f'=== {arch} t{tid} len={len(raw)} hdr={raw[:14].hex()} footer={raw[-8:].hex()}')
    for (s,e) in ranges:
        b=raw[s:e]
        print(f'-- {label} [{s},{e}) len={e-s}')
        for i in range(0,len(b),16):
            print(f'   {i:4d}: {b[i:i+16].hex(" ")}  {b[i:i+16]!r}')

# table 8 language suffix structure
raw=load('client',8)
pos=14
for i in range(3):
    ln=struct.unpack_from('<I',raw,pos)[0]
    suf=raw[pos+4+ln:pos+4+ln+30]
    print('t8 row',i,'name',raw[pos+4:pos+4+ln],'suffix idx17 u32=',struct.unpack_from('<I',suf,17)[0])
    print('   suffix bytes:', ' '.join(f'{c:02x}' for c in suf))
    print('   idx17..30:', suf[17:].hex())
    pos+=4+ln+30
print()
print('17-aligned u32s of suffix row0:', [struct.unpack_from('<I',suf if False else raw,0)])
# print as triple from 17
pos=14
for i in range(4):
    ln=struct.unpack_from('<I',raw,pos)[0]
    suf=raw[pos+4+ln:pos+4+ln+30]
    tail=suf[17:]
    print('row',i,'tail13', tail.hex(), 'u32s', struct.unpack('<III',tail[:12]), 'marker', tail[12])
    pos+=4+ln+30
