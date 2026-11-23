import struct,sys,collections
sys.path.insert(0,r'D:\tmp2b\fm24\tools\python'); sys.path.insert(0,r'scripts')
import t112_fm24_reader as R, zstandard as z
ar={a:R.Archive(a) for a in ('server','client')}
d=z.ZstdDecompressor()
def body(arch,nm):
    a=ar[arch]; p=f'{arch}_db/{nm}.dat'; e=a.entries[p]; o=d.decompressobj(); return o.decompress(a.data[a.data_base+e['offset']:])

b=body('server','simple_vars'); N=len(b)
def tryp(hdr,kw,lw,foot):
    p=hdr; end=N-foot; keys=[]
    while p<end:
        if p+kw+lw>end: return None
        k=int.from_bytes(b[p:p+kw],'little') if kw else None
        L=int.from_bytes(b[p+kw:p+kw+lw],'little')
        if L>end-p-kw-lw: return None
        if kw: keys.append(k)
        p+=kw+lw+L
        if len(keys)>400000: return None
    if p!=end: return None
    return keys
hits=[]
for hdr in range(8,30):
    for kw in (0,1,2,4):
        for lw in (1,2,3,4):
            for foot in range(0,14):
                r=tryp(hdr,kw,lw,foot)
                if r is not None:
                    mono=all(r[i]<r[i+1] for i in range(len(r)-1)) if r else True
                    hits.append((hdr,kw,lw,foot,len(r),len(set(r)),mono,max(r) if r else 0))
for h in hits: print('hdr=%d kw=%d lw=%d foot=%d recs=%d uniq=%d mono=%s maxkey=%d'%h)
print('nohit' if not hits else '')
