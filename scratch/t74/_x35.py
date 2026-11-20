import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

# ---- t18 exact formula test
for arch,const in (('client',65),('server',71)):
    raw=load(arch,18)
    p,b,_,_=dp_walk(raw,f'{arch}18',14,len(raw)-8,1567)
    rows=[(x[0],x[1]) for x in b]
    ok=0; bad=[]
    for i,(s,e) in enumerate(rows):
        # parse k strings
        q=s; tot=0; k=0
        while True:
            if q+4>e: break
            n=struct.unpack_from('<I',raw,q)[0]
            if n>4096 or q+4+n>e: break
            try: txt=raw[q+4:q+4+n].decode('utf-8')
            except Exception: break
            if not txt.isprintable() or not txt: break
            q+=4+n; tot+=n; k+=1
            if k==8: break
        if q+ (const-65) +13==e and tot+const==(e-s):
            ok+=1
        else: bad.append((i,e-s,tot,k,q,const-65+13))
    print(f't18 {arch} formula rowlen==sum(strlen)+{const}: ok {ok}/1567 bad {len(bad)}', bad[:4])

# ---- t47 lcrg: 13B identity, check row lengths 41+5k
for arch in ('client','server'):
    raw=load(arch,47)
    p,b,_,_=dp_walk(raw,f'{arch}47',14,len(raw)-8,2488)
    rows=[(x[0],x[1]) for x in b]
    lens=[e-s for s,e in rows]
    ks=collections.Counter()
    for L in lens:
        ks[(L-41)%5 if L>=41 else 'lt']+=1
    print(f't47 {arch}: rows {len(rows)} closure {rows[-1][1]==len(raw)-8} len min/max {min(lens)}/{max(lens)} (L-41)%5 dist {dict(ks)}')
