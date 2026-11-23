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

def parse(raw, maxtr=4, maxf=12):
    L=len(raw)
    if L<12 or raw[:8]!=MAGIC: return {'ok':False,'why':'header'}
    cnt=u32(raw,8)
    if cnt==0: return {'ok':L==12,'cnt':0,'n':0}
    memo={}
    def go(i,p):
        if (i,p) in memo: return memo[(i,p)]
        memo[(i,p)]=False
        if i==cnt: return p==L
        if p+4>L: return False
        uid=u32(raw,p)
        # candidate record ends: sequences of fields, prefer contiguous
        cands=[]
        def dfs(q,nf):
            if q<=L:
                cands.append((q,nf))
            if nf>=maxf or q>=L: return
            for fo in (0,1):
                v=str_at(raw,q+fo)
                if v is None: continue
                dfs(q+fo+4+v[0],nf+1)
        dfs(p+4,0)
        cands.sort(key=lambda c:(c[0], -c[1]))
        for e,nf in cands:
            for tr in range(maxtr+1):
                nxt=e+tr
                if nxt>L: break
                if go(i+1,nxt):
                    memo[(i,p)]=(uid,nf,tr,nxt)
                    return memo[(i,p)]
        return False
    r=go(0,12)
    return {'ok':bool(r),'cnt':cnt,'states':len(memo)}

if __name__=='__main__':
    ok=0; bad=[]; t=time.time()
    ns=names()
    for n in ns:
        raw=load(n); r=parse(raw)
        if r['ok']: ok+=1
        else: bad.append((n,r.get('why') or f"cnt={r.get('cnt')}"))
    print(f"closed {ok}/{len(ns)} in {time.time()-t:.1f}s")
    print('unclosed',len(bad),bad[:8])
