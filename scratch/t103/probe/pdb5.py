import sys, struct
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import zstandard as zstd
raw=open('scratch/data/people_db.dat','rb').read()
i=raw.find(b'\x28\xb5\x2f\xfd')
out=bytearray(); data=raw[i:]
while data[:4]==b'\x28\xb5\x2f\xfd':
    o=zstd.ZstdDecompressor().decompressobj(); out+=o.decompress(data)
    if not o.eof: break
    data=o.unused_data
    if not data: break
p=bytes(out); N=len(p)
print('N',N,'count@2',struct.unpack_from('<I',p,2)[0])
for a in range(0,160,8):
    print('%04x'%a, p[a:a+8].hex(' '), struct.unpack_from('<II',p,a))
