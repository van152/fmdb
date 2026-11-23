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
pos=5; bp_rows={}
for i in range(cnt):
    c=bp[pos+1]; L=CL[c]
    if c==5:
        o,d1,d2=struct.unpack_from('<III',bp,pos+L-12)
        bp_rows[o]=(d1,d2,pos)
    pos+=L
print('bp class5 rows',len(bp_rows), 'ord range',min(bp_rows),max(bp_rows))
p=dec('scratch/data/people_db.dat')
n=struct.unpack_from('<I',p,2)[0]
print('people count',n)
pos=6; ok=0; bad=0; k=0
rows=[]
while k<3000:
    key=struct.unpack_from('<I',p,pos)[0]
    cls=p[pos+4]; ln=struct.unpack_from('<I',p,pos+9)[0]
    ne=pos+13+ln
    q=ne; f=None
    while q<ne+64 and q+12<=len(p):
        if struct.unpack_from('<I',p,q)[0]==key and p[q+4:q+8]==p[q+8:q+12]: f=q; break
        q+=1
    if f is None: break
    tr=struct.unpack_from('<III',p,f)
    rows.append((key,cls,ln,tr))
    if key in bp_rows:
        if bp_rows[key][0]==tr[1] and bp_rows[key][1]==tr[2]: ok+=1
        else: bad+=1
    pos=f+12; k+=1
print('parsed',k,'key-in-bp',ok+bad,'duni match',ok,'mismatch',bad)
print('sample',rows[:3])
print('cls dist',Counter(r[1] for r in rows))
print('key==bp ordinal?', sum(1 for r in rows if r[0] in bp_rows), 'of', len(rows))
