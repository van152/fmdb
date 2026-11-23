import sys,struct,time
sys.path.insert(0,'scratch/t99')
from ld import load,names
def u32(b,p): return struct.unpack_from('<I',b,p)[0] if p+4<=len(b) else None
def tok(raw,p):
    if p+4>len(raw): return None
    ln=struct.unpack_from('<I',raw,p)[0]
    if ln>1024 or p+4+ln>len(raw): return None
    try: s=raw[p+4:p+4+ln].decode('utf-8')
    except UnicodeDecodeError: return None
    if ln and not all(c.isprintable() for c in s): return None
    return ln
def variants(raw,p,nf,T,policy,cap=4000):
    out=set(); cur={p+4}; n=0
    while cur and n<nf:
        nxt=set()
        for q in cur:
            ln=tok(raw,q)
            if ln is None: continue
            e=q+4+ln
            if policy=='opt':
                nxt.add(e)
                if e<len(raw): nxt.add(e+1)
            elif policy=='iflen':
                if ln==0: nxt.add(e)
                elif e<len(raw): nxt.add(e+1)
            else:
                if e<len(raw): nxt.add(e+1)
        n+=1
        for q in nxt:
            if q+T<=len(raw): out.add(q+T)
        cur=nxt
        if len(cur)>cap: return None
    return out
def walk(raw,nf,T,policy,cap=6000):
    cnt=u32(raw,8); L=len(raw); cur={(12,-1)}
    for i in range(cnt):
        nxt=set()
        for p,pu in cur:
            u=u32(raw,p)
            if u is None or u<=pu: continue
            vs=variants(raw,p,nf,T,policy)
            if vs is None: return None
            for e in vs:
                if i+1<cnt:
                    if e+4>L: continue
                elif e!=L: continue
                nxt.add((e,u))
        if not nxt or len(nxt)>cap: return None
        cur=nxt
    return any(p==L for p,_ in cur)
if __name__=='__main__':
    ns=names(); t=time.time(); res={}
    for n in ns:
        raw=load(n); hit=None
        for policy in ('opt','iflen','always'):
            for nf in range(1,11):
                for T in range(0,11):
                    if walk(raw,nf,T,policy): hit=(policy,nf,T); break
                if hit: break
            if hit: break
        res[n]=hit
    ok=sum(1 for v in res.values() if v)
    print(f"closed {ok}/{len(ns)} in {time.time()-t:.1f}s")
    import collections
    print('grammars',collections.Counter(res.values()).most_common(8))
    print('bad',[n for n,v in res.items() if not v])
