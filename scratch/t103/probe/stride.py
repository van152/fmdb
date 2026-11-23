import sys, struct
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import zstandard as zstd, numpy as np
def dec(p):
    raw=open(p,'rb').read(); i=raw.find(b'\x28\xb5\x2f\xfd')
    out=bytearray(); data=raw[i:]
    while data[:4]==b'\x28\xb5\x2f\xfd':
        o=zstd.ZstdDecompressor().decompressobj(); out+=o.decompress(data)
        if not o.eof: break
        data=o.unused_data
        if not data: break
    return bytes(out)
dt=dec('scratch/data/non_pl_hist_dt.dat')
print('len',len(dt))
for stride in (24,36,32,28,20,40):
    n=len(dt)//stride
    print('-- stride',stride,'n',n,'rem',len(dt)%stride)
    u=np.frombuffer(dt[:n*stride],dtype='<u4').reshape(n,stride//4).astype(np.uint64)
    offs=np.arange(n,dtype=np.uint64)*stride
    for w in range(stride//4):
        col=u[:,w]
        eq=int((col==offs+stride).sum()); nil=int((col==0xffffffff).sum())
        if eq>n*0.1 or nil>n*0.1:
            print('   word%d off%d: self+stride %d  nil %d  (%.3f/%.3f)'%(w,w*4,eq,nil,eq/n,nil/n))
