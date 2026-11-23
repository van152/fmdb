import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections, itertools

def mids(arch):
    raw=load(arch,7)
    p,b,_,_=dp_walk(raw,f'{arch}7',14,len(raw)-8,208)
    rows=[(x[0],x[1]) for x in b]
    out=[]
    for i,(s,e) in enumerate(rows):
        nl=struct.unpack_from('<I',raw,s)[0]
        q0=s+4+nl
        # find url lstr: first u32 after q0+2..q0+10 that forms an ascii url
        u=None
        for cand in range(q0,q0+12):
            L=struct.unpack_from('<I',raw,cand)[0]
            if L==0: u=(cand,0); break
            if 5<L<300 and cand+4+L<=e:
                try: t=raw[cand+4:cand+4+L].decode('ascii')
                except Exception: continue
                if t.startswith('http'): u=(cand,L); break
        pre=q0; upos,ul=u
        out.append((raw, s, e, pre, upos+4+ul, e-13))
    return out

for arch in ('client','server'):
    M=mids(arch)
    print('===',arch)
    for i in (0,16,29):
        raw,s,e,pre,ms,me=M[i]
        mid=raw[ms:me]
        print(f' row{i} rowlen={e-s} pre={raw[pre:ms].hex()} midlen={len(mid)}')
        for j in range(0,len(mid),16):
            print(f'   {j:4d} {mid[j:j+16].hex(" ")}')
