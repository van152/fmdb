import sys, struct
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import zstandard as zstd
raw=open('scratch/data/people_db.dat','rb').read()
print('raw',len(raw),'hdr',raw[:10].hex(' '))
i=raw.find(b'\x28\xb5\x2f\xfd')
out=bytearray(); data=raw[i:]
while data[:4]==b'\x28\xb5\x2f\xfd':
    o=zstd.ZstdDecompressor().decompressobj(); out+=o.decompress(data)
    if not o.eof: break
    data=o.unused_data
    if not data: break
p=bytes(out)
print('payload',len(p))
print('p[:200]', p[:200].hex(' '))
print('p[:200] repr', p[:200])
print('u32@0',struct.unpack_from('<I',p,0)[0], 'u32@2',struct.unpack_from('<I',p,2)[0])
# look for the trailer sig b600e207 / 01006c07
for sig in (b'\xb6\x00\xe2\x07', b'\x01\x00\x6c\x07'):
    print(sig.hex(), 'count', p.count(sig), 'first', p.find(sig))
print('tail', p[-80:].hex(' '))
