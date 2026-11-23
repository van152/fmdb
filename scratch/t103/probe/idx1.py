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
for tag,stride in (('pl',44),('non_pl',24)):
    idx=dec(f'scratch/data/{tag}_hist_index.dat')
    c=struct.unpack_from('<I',idx,0)[0]
    a=np.frombuffer(idx[4:4+8*c],dtype='<u4').reshape(c,2)
    print('==',tag,'index count',c,'keys uniq',len(np.unique(a[:,0])),'keys sorted',bool(np.all(np.diff(a[:,0].astype(np.int64))>0)))
    print('   val 0xffffffff',int((a[:,1]==0xffffffff).sum()),'vals uniq',len(np.unique(a[:,1])))
    print('   first 12',a[:12].tolist())
    # sorted-ness of keys as int
    k=a[:,0].astype(np.int64); d=np.diff(k)
    print('   min diff',int(d.min()),'neg count',int((d<0).sum()))
    # check if it's actually two interleaved arrays
    ids=open(f'scratch/data/{tag}_hist_id.dat','rb').read()
    print('   id header',ids[:12].hex(' '),'len',len(ids),'u32 after 8',(len(ids)-8)//4,'after 12',(len(ids)-12)//4)
    for hdr in (8,12):
        v=np.frombuffer(ids[hdr:],dtype='<u4').astype(np.int64)
        if len(v)%2: print('   odd'); continue
        p=v.reshape(-1,2)
        w=p[:,1]-p[:,0]
        print('   hdr',hdr,'pairs',len(p),'width min/max',int(w.min()),int(w.max()),'w0',int((w==0).sum()),'waligned',int((w%stride==0).sum()))
        print('      first 4',p[:4].tolist(),'last 2',p[-2:].tolist())
        print('      heads uniq',len(np.unique(p[:,0])),'sorted heads',bool(np.all(np.diff(p[:,0])>0)))
