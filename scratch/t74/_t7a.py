import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections, json

def rows7(arch):
    raw=load(arch,7)
    _,b,_,_=dp_walk(raw,f'{arch}7',14,len(raw)-8,208)
    return raw,[(x[0],x[1]) for x in b]

def layout(raw,rows):
    out=[]
    for i,(s,e) in enumerate(rows):
        nl=struct.unpack_from('<I',raw,s)[0]
        q=s+4+nl
        # 6B prefix then url lstr
        L=struct.unpack_from('<I',raw,q+6)[0]
        up=q+6+4+L
        ms=up; me=e-13
        sols=[]
        for H in range(0,40):
            if ms+H+4>me: break
            c=struct.unpack_from('<I',raw,ms+H)[0]
            if not (0<=c<400): continue
            if ms+H+4+c*12+5!=me: continue
            items=[struct.unpack_from('<III',raw,ms+H+4+12*k) for k in range(c)]
            if any(it[2]!=0 for it in items): continue
            sols.append((H,c,items))
        out.append((s,e,nl,q,ms,me,sols))
    return out

for arch in ('client','server'):
    raw,rows=rows7(arch)
    L=layout(raw,rows)
    print(arch,'sol-count dist',dict(collections.Counter(len(x[6]) for x in L)))
    Hs=collections.Counter(x[6][0][0] for x in L if len(x[6])==1)
    print('  H dist',dict(Hs))
    # head signature
    sig=collections.Counter()
    for x in L:
        if len(x[6])!=1: continue
        s,e,nl,q,ms,me,sols=x; H,c,items=sols[0]
        sig[(raw[ms:ms+H].hex(), me-(ms+H+4+c*12))]+=1
    print('  (head_hex, taillen) top:')
    for k,v in sig.most_common(6): print('   ',v,k)
