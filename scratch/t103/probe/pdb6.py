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
count=struct.unpack_from('<I',p,2)[0]
pos=6
rows=[]
for k in range(1000):
    key=struct.unpack_from('<I',p,pos)[0]
    cls=p[pos+4]
    f5=struct.unpack_from('<I',p,pos+5)[0]
    ln=struct.unpack_from('<I',p,pos+9)[0]
    nm=p[pos+13:pos+13+ln]
    ne=pos+13+ln
    # find footer: key then dup
    f=None
    q=ne
    while q<ne+40 and q+12<=N:
        if struct.unpack_from('<I',p,q)[0]==key and p[q+4:q+8]==p[q+8:q+12]:
            f=q; break
        q+=1
    if f is None: print('no footer at row',k,pos); break
    gap=p[ne:f]
    rows.append(dict(k=k,pos=pos,key=key,cls=cls,f5=f5,ln=ln,name=nm.decode('utf-8','replace'),ne=ne,f=f,gap=len(gap),gapnonnull=sum(1 for c in gap if c),next= f+12))
    pos=f+12
print('parsed',len(rows),'of 1000')
for r in rows[:6]: print(r)
from collections import Counter
print('cls',Counter(r['cls'] for r in rows))
print('f5',Counter(r['f5'] for r in rows).most_common(5))
print('gap',Counter(r['gap'] for r in rows).most_common(8))
print('gapnonnull',Counter(r['gapnonnull'] for r in rows).most_common(5))
# check the byte at footer end vs next key
bad=0
for r in rows[:200]:
    if p[r['next']:r['next']+4]!=struct.pack('<I', struct.unpack_from('<I',p,r['next'])[0]): bad+=1
print('rows where next pos is a key start:', sum(1 for r in rows[:200] if r['next']==r['f']+12))
