import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, hashlib, collections, json

def lstr(raw,q,e):
    if q+4>e: return None
    n=struct.unpack_from('<I',raw,q)[0]
    if n>4096 or q+4+n>e: return None
    try: t=raw[q+4:q+4+n].decode('utf-8')
    except Exception: return None
    if not t or not t.isprintable(): return None
    return q+4+n,n,t

out={}
# t47: 41+5k
for arch in ('client','server'):
    raw=load(arch,47); H,F=14,len(raw)-8
    p=H;i=0;lens=[];bad=0
    while p<F:
        L=struct.unpack_from('<I',raw,p)[0]
        # length prefix at row start? unknown; use 41+5k rule: need k from content
        break
    # use DP rows
    _,b,_,_=dp_walk(raw,f'{arch}47',H,F,2488)
    rows=[(x[0],x[1]) for x in b]
    lens=[e-s for s,e in rows]
    bad=0
    for i,(s,e) in enumerate(rows):
        o,u1,u2=struct.unpack_from('<III',raw,e-13)
        if not(o==i and u1==u2 and raw[e-1]==0): bad+=1
    out[f'47_{arch}']=dict(payload=len(raw),rows=len(rows),closure=rows[-1][1]==F,
        lens=(min(lens),max(lens)),mod5=dict(collections.Counter((L-41)%5 for L in lens)),
        bad=bad,sha=hashlib.sha256(raw).hexdigest(),
        hist={str(k):v for k,v in sorted(collections.Counter(lens).items())})
# t18
for arch in ('client','server'):
    raw=load(arch,18); H,F=14,len(raw)-8
    _,b,_,_=dp_walk(raw,f'{arch}18',H,F,1567)
    rows=[(x[0],x[1]) for x in b]
    const=65 if arch=='client' else 71
    ok=0;ks=collections.Counter();lens=[];bad=0
    for i,(s,e) in enumerate(rows):
        q=s;tot=0;k=0
        while k<8:
            r=lstr(raw,q,e)
            if not r: break
            q,n,t=r; tot+=n;k+=1
        if e-s==tot+const: ok+=1
        ks[k]+=1; lens.append(e-s)
        o,u1,u2=struct.unpack_from('<III',raw,e-13)
        if not(o==i and u1==u2 and raw[e-1]==0): bad+=1
    out[f'18_{arch}']=dict(payload=len(raw),rows=len(rows),closure=rows[-1][1]==F,
        formula_ok=f'{ok}/1567',const=const,k=dict(ks),bad_identity=bad,
        lens=(min(lens),max(lens)),sha=hashlib.sha256(raw).hexdigest(),
        hist={str(k2):v for k2,v in sorted(collections.Counter(lens).items())})
print(json.dumps(out,ensure_ascii=False)[:1600])
open('scratch/t74/_stats_a.json','w').write(json.dumps(out,ensure_ascii=False))
