import sys,struct,time
sys.path.insert(0,'scratch/t99')
from ld import load,names
def u32(b,p): return struct.unpack_from('<I',b,p)[0] if p+4<=len(b) else None
def str_at(raw,r):
    if r+4>len(raw): return None
    ln=u32(raw,r)
    if ln>4096 or r+4+ln>len(raw): return None
    try: s=raw[r+4:r+4+ln].decode('utf-8')
    except UnicodeDecodeError: return None
    if ln and not all(c.isprintable() for c in s): return None
    return ln
def tagok(b): return b<0x40 or b==0xff
def item_ends(raw,p,window,maxitems,gapmax):
    L=len(raw); ends={p:0}; frontier={p:0}
    while frontier:
        nxt={}
        for q,nf in frontier.items():
            if nf>=maxitems or q-p>window: continue
            for g in range(gapmax+1):
                if g and not all(tagok(c) for c in raw[q:q+g]): break
                ln=str_at(raw,q+g)
                if ln is None: continue
                e=q+g+4+ln
                if e>L: continue
                if ends.get(e,99)>nf+1:
                    ends[e]=nf+1; nxt.setdefault(e,nf+1)
        frontier=nxt
    return ends
def parse(raw,gapmax=3,window=9000,maxitems=48,maxtr=8):
    L=len(raw); cnt=u32(raw,8)
    if cnt==0: return (L==12,None)
    layer={12:None}
    for i in range(cnt):
        nxt={}
        for p in layer:
            u=u32(raw,p)
            if u is None: continue
            for e,nf in item_ends(raw,p+4,window,maxitems,gapmax).items():
                for tr in range(maxtr+1):
                    q=e+tr
                    if q>L: break
                    if i+1<cnt:
                        v=u32(raw,q)
                        if v is None or v<=u: continue
                    elif q!=L: continue
                    nxt.setdefault(q,None)
        if not nxt or len(nxt)>80000: return (False,i)
        layer=nxt
    return (L in layer,None)
if __name__=='__main__':
    for n in sys.argv[1:]:
        raw=load(n); t=time.time(); r=parse(raw)
        print(f"{n:26s} cnt={u32(raw,8):5d} -> {r} {time.time()-t:.1f}s")
