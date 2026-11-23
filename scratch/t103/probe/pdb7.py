import sys, struct
from collections import Counter
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
count=struct.unpack_from('<I',p,2)[0]
pos=6; k=0
cls=Counter(); gaps=Counter(); f5=Counter(); keys=[]; name_len=[]; duni=[]; bad=[]
while k<count:
    key=struct.unpack_from('<I',p,pos)[0]
    c=p[pos+4]; v=struct.unpack_from('<I',p,pos+5)[0]; ln=struct.unpack_from('<I',p,pos+9)[0]
    ne=pos+13+ln
    cls[c]+=1; f5[v]+=1; name_len.append(ln)
    duni.append(struct.unpack_from('<I',p,ne+8+8)[0] if False else 0)
    # footer search
    q=ne; found=None
    while q<ne+64 and q+12<=N:
        if struct.unpack_from('<I',p,q)[0]==key and p[q+4:q+8]==p[q+8:q+12]:
            found=q; break
        q+=1
    if found is None:
        bad.append((k,pos,key)); break
    gaps[found-ne]+=1
    keys.append((key, struct.unpack_from('<I',p,found+4)[0]))
    pos=found+12; k+=1
print('rows parsed',k,'of',count,'end pos',pos,'N',N,'trailing',N-pos)
print('trailing bytes',p[pos:pos+32].hex(' '))
print('cls',cls)
print('f5 top',f5.most_common(5))
print('gaps',gaps.most_common(8))
print('name_len min/max',min(name_len),max(name_len))
print('bad',bad[:3])
k2=[a for a,b in keys]; d=[b for a,b in keys]
print('key distinct',len(set(k2)),'min',min(k2),'max',max(k2))
print('duni distinct',len(set(d)),'zero',d.count(0))
print('first keys',k2[:6],'first duni',d[:6])
