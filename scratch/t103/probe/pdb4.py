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
def try_parse(start, pre_u32):
    pos=start; rows=[]
    while pos < N-1:
        if pos+9+12 > N: return rows,'overrun',pos
        key=struct.unpack_from('<I',p,pos)[0]
        if pre_u32:
            if pos+13 > N: return rows,'overrun2',pos
            cls=p[pos+8]; ln=struct.unpack_from('<I',p,pos+9)[0]; nameoff=pos+13
        else:
            cls=p[pos+4]; ln=struct.unpack_from('<I',p,pos+5)[0]; nameoff=pos+9
        if cls==0 or cls>8: return rows,('badcls',cls),pos
        if ln>200: return rows,('badlen',ln),pos
        if nameoff+ln>N: return rows,'nameover',pos
        nm=p[nameoff:nameoff+ln]
        if any(c<0x20 for c in nm): return rows,('badname',nm[:10]),pos
        q=nameoff+ln
        # skip zero pad
        z=q
        while z<N and p[z]==0: z+=1
        if z+12>N: return rows,'trailover',pos
        t=struct.unpack_from('<III',p,z)
        if t[1]!=t[2]: return rows,('trailmismatch',t),pos
        rows.append((key,cls,ln,z+12))
        pos=z+12
        if len(rows)>3000: return rows,'cap',pos
    return rows,'end',pos
for pre in (True,False):
    r,why,pos=try_parse(2,pre)
    print('pre_u32',pre,'rows',len(r),'stop',why,'pos',pos)
    if r: print('   last',r[-1])
