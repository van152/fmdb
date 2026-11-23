import sys, struct
from collections import Counter
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
pos=5; order=[]
for i in range(cnt):
    c=bp[pos+1]; L=CL[c]
    f=pos+L-12; order.append((struct.unpack_from('<I',bp,f)[0], bp[f:f+12], c, L))
    pos+=L
print('bp rows',len(order),'end',pos)
p=dec('scratch/data/people_db.dat')
pos=6; k=0; bad=0; lens=Counter(); bodylen={}
import collections
bd=collections.defaultdict(Counter)
while k<len(order):
    key,foot,c,L=order[k]
    j=p.find(foot,pos)
    if j<0 or j>pos+20000:
        bad+=1; print('stop at',k,'pos',pos,'key',key,'cls',c,'found',j); break
    lens[j+12-pos]+=1; bd[c][j-(pos+5)]+=1
    pos=j+12; k+=1
print('walked',k,'pos',pos,'len',len(p),'remain',len(p)-pos)
for c in sorted(bd): print('cls',c,'n',sum(bd[c].values()),'bodylen',bd[c].most_common(6))
