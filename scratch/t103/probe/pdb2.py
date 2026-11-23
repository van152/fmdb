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
p=bytes(out)
n=struct.unpack_from('<I',p,2)[0]
print('count',n,'len',len(p))
# hypothesised row: u32 key, u32 sid, u8 cls=05, u8 pad, u32 name_len, name, pad-to-4?, then 12B trailer (key,duni,duni)
pos=6
rows=[]
for k in range(12):
    print('--- row',k,'at',pos)
    print('   ', p[pos:pos+72].hex(' '))
    key,sid = struct.unpack_from('<II',p,pos)
    cls = p[pos+8]; pad=p[pos+9]
    ln = struct.unpack_from('<I',p,pos+10)[0]
    nm = p[pos+14:pos+14+ln]
    print('   key=%d sid=0x%x cls=%d pad=%d len=%d name=%r'%(key,sid,cls,pad,ln,nm))
    nxt = pos+14+ln
    # pad to 4
    nxt4 = (nxt+3)&~3
    print('   after name',nxt,'aligned',nxt4,'bytes',p[nxt:nxt4+12].hex(' '))
    tr = struct.unpack_from('<III',p,nxt4)
    print('   trailer',tr)
    pos = nxt4+12
    rows.append((key,sid,cls,ln,nm))
