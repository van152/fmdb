import sys, struct
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
pos=5; rows={}
for i in range(cnt):
    c=bp[pos+1]; L=CL[c]; rows[struct.unpack_from('<I',bp,pos+L-12)[0]]=(pos,L,c)
    pos+=L
p=dec('scratch/data/people_db.dat')
pos=6
for t in range(3):
    key=struct.unpack_from('<I',p,pos)[0]; ln=struct.unpack_from('<I',p,pos+9)[0]
    ne=pos+13+ln; q=ne
    while struct.unpack_from('<I',p,q)[0]!=key or p[q+4:q+8]!=p[q+8:q+12]: q+=1
    pp,L,c=rows[key]
    print('--- key',key,'cls',c,'pdb_rowlen',q+12-pos,'bp_rowlen',L)
    print(' pdb',p[pos:q+12].hex(' '))
    print(' bp ',bp[pp:pp+L].hex(' '))
    pos=q+12
