import sys,struct,time
sys.path.insert(0,'scratch/t99')
from ld import load,names
MAGIC=bytes.fromhex('03017461642ef10d')
def u32(b,p): return struct.unpack_from('<I',b,p)[0] if p+4<=len(b) else None
def tagok(c): return c<=0x1f or c==0xff
def str_at(raw,r):
    if r+4>len(raw): return None
    ln=u32(raw,r)
    if ln>2048 or r+4+ln>len(raw): return None
    try: s=raw[r+4:r+4+ln].decode('utf-8')
    except UnicodeDecodeError: return None
    if ln and not all(ch.isprintable() for ch in s): return None
    return ln
def item_ends(raw,p,window,maxitems=32):
    L=len(raw); ends={p:0}; frontier={p:0}
    while frontier:
        nxt={}
        for q,nf in frontier.items():
            if nf>=maxitems or q-p>window: continue
            for b in range(0,4):
                if b and not all(tagok(c) for c in raw[q:q+b]): break
                ln=str_at(raw,q+b)
                if ln is None: continue
                e=q+b+4+ln
                if e>L: continue
                if ends.get(e,99)>nf+1:
                    ends[e]=nf+1; nxt.setdefault(e,nf+1)
        frontier=nxt
    return ends
def parse(raw,window=8000,maxitems=32,maxtr=4):
    L=len(raw); cnt=u32(raw,8)
    if cnt==0: return L==12
    layer={12:None}
    for i in range(cnt):
        nxt={}
        for p in layer:
            u=u32(raw,p)
            if u is None: continue
            for e in item_ends(raw,p+4,window,maxitems):
                for tr in range(maxtr+1):
                    q=e+tr
                    if q>L: break
                    if i+1<cnt:
                        v=u32(raw,q)
                        if v is None or v<=u: continue
                    elif q!=L: continue
                    nxt.setdefault(q,None)
        if not nxt or len(nxt)>60000: return False
        layer=nxt
    return L in layer
if __name__=='__main__':
    ns=names() if len(sys.argv)<2 else sys.argv[1:]
    ok=0; bad=[]; t=time.time()
    for n in ns:
        r=parse(load(n))
        if r: ok+=1
        else: bad.append(n)
    print(f"closed {ok}/{len(ns)} in {time.time()-t:.1f}s bad={bad}")
