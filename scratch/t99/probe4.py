import sys,struct,time
sys.path.insert(0,'scratch/t99')
from ld import load,names
MAGIC=bytes.fromhex('03017461642ef10d')
def u32(b,p): return struct.unpack_from('<I',b,p)[0]

def str_at(raw,r):
    if r+4>len(raw): return None
    ln=u32(raw,r)
    if ln>1024 or r+4+ln>len(raw): return None
    try: s=raw[r+4:r+4+ln].decode('utf-8')
    except UnicodeDecodeError: return None
    if ln and not all(c.isprintable() for c in s): return None
    return ln,s

def field_ends(raw,p,uid,L,maxf=12,window=3000):
    """all positions reachable by 0..maxf fields from p (record start)."""
    ends={}
    frontier={p+4:0}
    ends[p+4]=0
    while frontier:
        nxt={}
        for q,nf in frontier.items():
            if nf>=maxf or q>=L or q-p>window: continue
            for fo in (0,1):
                v=str_at(raw,q+fo)
                if v is None: continue
                e=q+fo+4+v[0]
                if e>L: continue
                if ends.get(e,99)>nf+1:
                    ends[e]=nf+1; nxt[e]=nf+1
        frontier=nxt
    return ends

def parse(raw,maxtr=4,maxf=12):
    L=len(raw)
    if L<12 or raw[:8]!=MAGIC: return {'ok':False,'why':'header'}
    cnt=u32(raw,8)
    if cnt==0: return {'ok':L==12,'cnt':0,'n':0}
    layer={12:None}
    for i in range(cnt):
        nxt={}
        for p in layer:
            if p+4>L: continue
            uid=u32(raw,p)
            ends=field_ends(raw,p,uid,L,maxf)
            for e,nf in ends.items():
                for tr in range(maxtr+1):
                    q=e+tr
                    if q>L: break
                    if i+1<cnt:
                        if q+4>L or u32(raw,q)<=uid: continue
                    else:
                        if q!=L: continue
                    if q not in nxt: nxt[q]=(p,uid,nf,tr)
        if not nxt: return {'ok':False,'why':f'dead at rec {i}/{cnt}','layer':len(layer)}
        if len(nxt)>20000: return {'ok':False,'why':f'explode {len(nxt)} at rec {i}'}
        layer=nxt
    return {'ok':L in layer,'cnt':cnt,'layer':len(layer)}

if __name__=='__main__':
    ns=names(); ok=0; bad=[]; t=time.time()
    for n in ns:
        r=parse(load(n))
        if r['ok']: ok+=1
        else: bad.append((n,r.get('why')))
    print(f"closed {ok}/{len(ns)} in {time.time()-t:.1f}s")
    for b in bad[:20]: print('  ',b)
