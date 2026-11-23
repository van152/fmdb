import sys, struct, json
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
bp=dec('scratch/data/basic_people_db.dat')
CL={1:83,2:83,3:83,4:34,5:22}
cnt=struct.unpack_from('<I',bp,0)[0]
pos=5; kmap={}; bpc=Counter()
for i in range(cnt):
    c=bp[pos+1]; L=CL[c]
    f=pos+L-12
    k=struct.unpack_from('<I',bp,f)[0]; d=struct.unpack_from('<I',bp,f+4)[0]
    kmap[k]=d; bpc[c]+=1
    pos+=L
print('bp rows',len(kmap),'end',pos,'classes',dict(bpc))
p=dec('scratch/data/people_db.dat')
n=struct.unpack_from('<I',p,2)[0]
pos=6; k=0; cls=Counter(); body=defaultdict(Counter); errs=[]
while k<n:
    key=struct.unpack_from('<I',p,pos)[0]
    if key not in kmap: errs.append(('unknown key',k,pos,key)); break
    c=p[pos+4]; d=kmap[key]
    pat=struct.pack('<III',key,d,d)
    j=p.find(pat,pos+5,pos+9000)
    if j<0: errs.append(('no trailer',k,pos,key)); break
    cls[c]+=1; body[c][j-(pos+5)]+=1
    pos=j+12; k+=1
print('walked',k,'pos',pos,'remain',len(p)-pos,'errs',errs[:3])
print('cls counts',dict(cls))
for c in sorted(body): print(' cls',c,'n',sum(body[c].values()),'bodylen',body[c].most_common(10))
json.dump({'rows':k,'cls':dict(cls),'body':{str(c):body[c].most_common(20) for c in body}},open('scratch/t103/probe/pdbwalk3.json','w'),indent=1)
