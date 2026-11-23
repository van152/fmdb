import sys, struct, collections
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import zstandard as zstd
def dec(path):
    raw=open(path,'rb').read(); i=raw.find(b'\x28\xb5\x2f\xfd')
    out=bytearray(); data=raw[i:]; ends=[]
    while data[:4]==b'\x28\xb5\x2f\xfd':
        o=zstd.ZstdDecompressor().decompressobj(); out+=o.decompress(data)
        used=len(data)-len(o.unused_data)
        if not o.eof: break
        data=o.unused_data; ends.append(used)
        if not data: break
    return raw, bytes(out), data
for tag,stride in (('pl',44),('non_pl',24)):
    raw,dt,left = dec(f'scratch/data/{tag}_hist_dt.dat')
    print('==',tag,'dt',len(dt),'stride',stride,'records',len(dt)/stride,'leftover',len(left))
    print('  leftover head',left[:48].hex(' '))
    print('  leftover tail',left[-48:].hex(' '))
    n=len(dt)//stride
    # chain test
    nxt=struct.unpack_from('<%dI'%n, dt, stride-4) if False else None
    import numpy as np
    arr=np.frombuffer(dt,dtype=np.uint8).reshape(n,stride)
    links=np.frombuffer(dt,dtype='<u4')[stride//4-1::stride//4]
    print('  links: n',len(links),'nil',int((links==0xffffffff).sum()),'valid',int((links%stride==0).sum()),'inbounds',int((links<len(dt)).sum()))
    nonnil=links[links!=0xffffffff]
    print('  nonnil % aligned %d/%d'%(int((nonnil%stride==0).sum()), len(nonnil)))
    # heads from id
    ids=open(f'scratch/data/{tag}_hist_id.dat','rb').read()[8:]
    a=np.frombuffer(ids,dtype='<u4')
    hs=a[0::2]; he=a[1::2]
    print('  id pairs',len(hs),'widths uni',sorted(set((he-hs).tolist()))[:4],'heads distinct',len(set(hs.tolist())),'head%aligned',int((hs%stride==0).sum()))
    print('  head min/max',int(hs.min()),int(hs.max()),'dt len',len(dt))
    heads=set(hs.tolist())
    # walk chains from heads
    seen=bytearray(n); total=0; bad=0; dup=0; over=0
    for h in list(heads)[:200000]:
        cur=h
        while True:
            if cur==0xffffffff: break
            if cur%stride or cur>=len(dt): over+=1; break
            r=cur//stride
            if seen[r]: dup+=1; break
            seen[r]=1; total+=1
            cur=int(links[r])
    print('  partial walk heads=200000 records',total,'dup',dup,'oob',over)
    print('  covered',sum(seen),'of',n)
