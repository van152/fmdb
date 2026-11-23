import sys, struct
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import zstandard as zstd, numpy as np
def dec(path):
    raw=open(path,'rb').read(); i=raw.find(b'\x28\xb5\x2f\xfd')
    out=bytearray(); data=raw[i:]
    while data[:4]==b'\x28\xb5\x2f\xfd':
        o=zstd.ZstdDecompressor().decompressobj(); out+=o.decompress(data)
        if not o.eof: break
        data=o.unused_data
        if not data: break
    return raw, bytes(out), data
for tag,stride in (('pl',44),('non_pl',24)):
    raw,dt,left = dec(f'scratch/data/{tag}_hist_dt.dat')
    n=len(dt)//stride
    links=np.frombuffer(dt,dtype='<u4')
    links=links.reshape(n,stride//4)[:, -1].astype(np.uint64)
    nonnil=links[links!=0xffffffff]
    print('==',tag,'records',n,'leftover',len(left),'nil',int((links==0xffffffff).sum()))
    print('   nonnil',len(nonnil),'aligned',int((nonnil%stride==0).sum()),'inbounds',int((nonnil<len(dt)).sum()))
    # heads
    ids=open(f'scratch/data/{tag}_hist_id.dat','rb').read()[8:]
    a=np.frombuffer(ids,dtype='<u4'); print('   id u32',len(a),'odd',len(a)%2)
    hs=a[0::2].astype(np.uint64); he=a[1::2].astype(np.uint64)
    print('   pairs',len(hs),'head aligned',int((hs%stride==0).sum()),'end aligned',int((he%stride==0).sum()))
    heads=np.unique(hs); print('   distinct heads',len(heads))
    idx_raw=dec(f'scratch/data/{tag}_hist_index.dat')[1]
    k=struct.unpack_from('<I',idx_raw,0)[0]
    pk=np.frombuffer(idx_raw[4:4+8*k],dtype='<u4').reshape(k,2).astype(np.uint64)
    print('   index n',k,'keys distinct',len(np.unique(pk[:,0])))
    print('   idx key == id head?', k==len(hs), 'eq frac', float((pk[:min(k,len(hs)),0]==hs[:min(k,len(hs))]).mean()) if k else None)
    # chain walk complete
    seen=np.zeros(n,dtype=np.uint8); total=0; dup=0; oob=0
    for h in heads.tolist():
        cur=h
        while cur!=0xffffffff:
            if cur%stride or cur>=len(dt): oob+=1; break
            r=cur//stride
            if seen[r]: dup+=1; break
            seen[r]=1; total+=1
            cur=int(links[r])
    print('   walk total',total,'dup',dup,'oob',oob,'covered',int(seen.sum()),'of',n)
