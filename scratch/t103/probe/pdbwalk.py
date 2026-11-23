import sys, struct
from collections import Counter, defaultdict
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import zstandard as zstd
def dec(p):
    raw=open(p,'rb').read(); i=raw.find(b'\x28\xb5\x2f\xfd')
    out=bytearray(); data=raw[i:]
    while data[:4]==b'\x28\xb5\x2f\xfd':
        o=zstd.ZstdDecompressor().decompressobj(); out+=o.decompress(data)
        if not o.eof: break
        data=o.unused_data
        if not data: break
    return bytes(out)
p=dec('scratch/data/people_db.dat')
n=struct.unpack_from('<I',p,2)[0]
print('count',n,'len',len(p))
pos=6; k=0; cls_bodies=defaultdict(Counter); bad=[]
keys=[]
while k<n:
    key=struct.unpack_from('<I',p,pos)[0]; cls=p[pos+4]
    q=pos+5; f=None
    lim=min(pos+9000,len(p)-12)
    while q<lim:
        if struct.unpack_from('<I',p,q)[0]==key and p[q+4:q+8]==p[q+8:q+12]:
            f=q; break
        q+=1
    if f is None: bad.append((k,pos,key,cls)); break
    cls_bodies[cls][f-(pos+5)]+=1
    keys.append(key); k+=1; pos=f+12
print('parsed',k,'endpos',pos,'remain',len(p)-pos)
print('bad',bad[:3])
for c in sorted(cls_bodies): print('cls',c,'bodylen top',cls_bodies[c].most_common(8))
print('key monotone?', all(keys[i]<keys[i+1] for i in range(len(keys)-1)))
print('first/last key',keys[0],keys[-1],'min',min(keys),'max',max(keys))
