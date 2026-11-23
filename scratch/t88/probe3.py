import struct
b=open('D:/tmp2b/fm24-db/scratch/t88/t45.bin','rb').read()
n=struct.unpack_from('<I',b,8)[0]
def d(o,k=16):
    return ' '.join(f'{o+i:02x}:{b[o+i]:02x}' for i in range(0,k))
for o in range(0,120,16):
    print(o, b[o:o+16].hex(' '))
print('...')
for o in range(len(b)-96,len(b),16):
    print(o, b[o:o+16].hex(' '))
# search for ordinal==0 aligned candidates
hits=[p for p in range(12,120) if struct.unpack_from('<I',b,p)[0]==0]
print('u32==0 in first 120:',hits)
