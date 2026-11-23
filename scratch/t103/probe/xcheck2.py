import sys, struct
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import zstandard as zstd
raw=open('scratch/data/people_db.dat','rb').read(); i=raw.find(b'\x28\xb5\x2f\xfd')
out=bytearray(); data=raw[i:]
while data[:4]==b'\x28\xb5\x2f\xfd':
    o=zstd.ZstdDecompressor().decompressobj(); out+=o.decompress(data)
    if not o.eof: break
    data=o.unused_data
    if not data: break
p=bytes(out); del out
pos=6; k=0
while k<1193:
    key=struct.unpack_from('<I',p,pos)[0]; ln=struct.unpack_from('<I',p,pos+9)[0]
    ne=pos+13+ln; q=ne
    while struct.unpack_from('<I',p,q)[0]!=key or p[q+4:q+8]!=p[q+8:q+12]: q+=1
    pos=q+12; k+=1
print('pos',pos,'nextkey',struct.unpack_from('<I',p,pos)[0])
print(p[pos:pos+64].hex(' '))
print('ascii',p[pos:pos+64])
