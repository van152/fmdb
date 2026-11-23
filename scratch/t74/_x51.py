import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

TAIL=b'\x00\x00\x00\x00\x01'

def walk(raw,p,me,stats):
    while p<me:
        if me-p==5:
            return p if raw[p:p+5]==TAIL else None
        if p+4>me: return None
        v=struct.unpack_from('<I',raw,p)[0]
        if v==0xffffffff:
            p+=4; stats['ff']+=1; continue
        if p+12<=me:
            a,b2,c=struct.unpack_from('<III',raw,p)
            if a==b2 and c==0 and 0<a<10**7:
                p+=12; stats['triple']+=1; continue
        if 0<v<400 and p+4+v<=me:
            seg=raw[p+4:p+4+v]
            try: t=seg.decode('utf-8')
            except Exception: t=None
            if t and t.isprintable() and sum(ch.isalnum() or ch in ' .-_/:,+&?=%#@()' for ch in t)>=len(t)*0.9:
                p+=4+v; stats['lstr']+=1; continue
        if v==0 and p+4<=me:
            p+=4; stats['zero']+=1; continue
        return None
    return None

def mids(arch):
    raw=load(arch,7)
    p,b,_,_=dp_walk(raw,f'{arch}7',14,len(raw)-8,208)
    rows=[(x[0],x[1]) for x in b]
    out=[]
    for i,(s,e) in enumerate(rows):
        nl=struct.unpack_from('<I',raw,s)[0]
        q=s+4+nl
        off=None; L=0
        for cand in range(q,q+16):
            v=struct.unpack_from('<I',raw,cand)[0]
            if v==0: off=cand; L=0; break
            if 4<v<300 and cand+4+v<=e:
                try: t=raw[cand+4:cand+4+v].decode('ascii')
                except Exception: continue
                if t.startswith('http'): off,L=cand,v; break
        out.append((s,e,q,off+4+L,e-13))
    return raw,out

for arch in ('client','server'):
    raw,M=mids(arch)
    fits=collections.Counter(); stats=collections.Counter(); fails=[]
    for i,(s,e,q,ms,me) in enumerate(M):
        cands=[]
        for H in range(0,44):
            if ms+H>me: break
            st=collections.Counter()
            r=walk(raw,ms+H,me,st)
            if r is not None and r==me:
                cands.append((H,tuple(sorted(st.items()))))
        fits[len(cands)]+=1
        if len(cands)==1:
            for k,v in cands[0][1]: stats[k]+=v
            stats[('H%d'%cands[0][0])]+=1
        else: fails.append((i,len(cands),me-ms,cands[:3]))
    print(arch,'fitcount dist',dict(fits))
    print('  stats',[ (k,v) for k,v in stats.most_common(14)])
    print('  fails',fails[:6])
