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
    return bytes(out)
for tag,stride in (('pl',44),('non_pl',24)):
    dt=dec(f'scratch/data/{tag}_hist_dt.dat')
    n=len(dt)//stride
    a=np.frombuffer(dt[:n*stride],dtype=np.uint8).reshape(n,stride)
    u=np.frombuffer(dt[:n*stride],dtype='<u4').reshape(n,stride//4)
    print('==',tag,'stride',stride,'n',n,'words',stride//4)
    offs=np.arange(n,dtype=np.uint64)*stride
    link=u[:,-1].astype(np.uint64)
    nil=(link==0xffffffff)
    print('  link nil',int(nil.sum()),'link==self+stride',int((link==offs+stride).sum()),'other',int((~nil & (link!=offs+stride)).sum()))
    # identity candidates: adjacent equal words
    for k in range(stride//4-1):
        eq=float((u[:,k]==u[:,k+1]).mean())
        if eq>0.9: print('   words %d,%d equal %.4f'%(k,k+1,eq))
    # index
    idx=dec(f'scratch/data/{tag}_hist_index.dat')
    c=struct.unpack_from('<I',idx,0)[0]
    pk=np.frombuffer(idx[4:4+8*c],dtype='<u4').reshape(c,2)
    print('  index n',c,'keys incr',bool(np.all(np.diff(pk[:,0].astype(np.int64))>0)),'vals max',int(pk[:,1].max()),'vals seq',bool(np.all(pk[:,1]==np.arange(c))))
    # id
    ids=open(f'scratch/data/{tag}_hist_id.dat','rb').read()[8:]
    v=np.frombuffer(ids,dtype='<u4').astype(np.uint64)
    print('  id n',len(v),'even',len(v)%2==0,'pairs',len(v)//2,'head%stride',int((v[0::2]%stride==0).sum()),'tail%stride',int((v[1::2]%stride==0).sum()))
    print('  id first 8',v[:8].tolist(),'last 4',v[-4:].tolist())
    # are heads == nil-link records? heads are chain ends?
    ends=set(offs[nil].tolist())
    print('  heads in ends', int(np.isin(v[0::2], list(ends)).sum()), 'of', len(v)//2)
    # chain length check: walk first 20 chains using head->link
    print('  sample walk:')
    for h in v[0::2][:6].tolist():
        cur=h; ln=0; path=[]
        while cur!=0xffffffff and ln<50:
            if cur%stride or cur>=len(dt): path.append('OOB'); break
            path.append(cur); cur=int(u[cur//stride,-1]); ln+=1
        print('    head',h,'len',ln,'path',path[:6])
