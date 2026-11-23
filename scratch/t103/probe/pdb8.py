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
# find first of each class
cnt=struct.unpack_from('<I',bp,0)[0]; pos=5; first={}
for i in range(cnt):
    c=bp[pos+1]; L=CL[c]
    if c not in first: first[c]=(i,pos)
    pos+=L
    if len(first)==5: break
for c,(i,p0) in sorted(first.items()):
    L=CL[c]; row=bp[p0:p0+L]
    print('=== class',c,'row',i,'len',L)
    for o in range(L):
        print('  %3d %02x'%(o,row[o]))
    break
