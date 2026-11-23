import sys, struct
sys.path.insert(0, r'D:\tmp2b\fm24\tools\python')
import zstandard as zstd
from collections import Counter
def dec(path):
    raw=open(path,'rb').read(); i=raw.find(b'\x28\xb5\x2f\xfd')
    out=bytearray(); data=raw[i:]; nf=0
    while data[:4]==b'\x28\xb5\x2f\xfd':
        o=zstd.ZstdDecompressor().decompressobj(); out+=o.decompress(data); nf+=1
        if not o.eof: break
        data=o.unused_data
        if not data: break
    return bytes(out), nf, len(data)
for tag in ('pl','non_pl'):
    dt,nf,left = dec(f'scratch/data/{tag}_hist_dt.dat')
    idx,_,_ = dec(f'scratch/data/{tag}_hist_index.dat')
    ids = open(f'scratch/data/{tag}_hist_id.dat','rb').read()[12:]
    print('==',tag,'dt',len(dt),'frames',nf,'left',left,'idx',len(idx),'ids',len(ids),'n_ids',len(ids)//4)
    n=struct.unpack_from('<I',idx,0)[0]
    print('  index count',n,'expected pairs bytes',4+8*n,'actual',len(idx),'diff',len(idx)-(4+8*n))
    pairs=[struct.unpack_from('<II',idx,4+8*i) for i in range(min(n,8))]
    print('  index head',pairs)
    pairs_all=[struct.unpack_from('<II',idx,4+8*i) for i in range(n)]
    print('  index key monotone', all(pairs_all[i][0]<pairs_all[i+1][0] for i in range(len(pairs_all)-1)))
    print('  index vals head', [p[1] for p in pairs_all[:12]], 'max', max(p[1] for p in pairs_all))
    a=struct.unpack_from('<%dI'%(len(ids)//4), ids, 0)
    print('  id min/max',a[0],a[-1],'monotone nondecr',all(a[i]<=a[i+1] for i in range(len(a)-1)))
    ps=[(a[i],a[i+1]) for i in range(0,len(a)-1,2)]
    print('  id pair count',len(ps),'head',ps[:5])
    widths=Counter(p[1]-p[0] for p in ps)
    print('  width hist',widths.most_common(8),'sum',sum(p[1]-p[0] for p in ps))
    gaps=Counter(ps[i+1][0]-ps[i][1] for i in range(len(ps)-1))
    print('  gap hist',gaps.most_common(6))
