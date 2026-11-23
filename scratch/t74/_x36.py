import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

def strs(raw,s,e,maxn=8):
    q=s; tot=0; k=0
    while k<maxn and q+4<=e:
        n=struct.unpack_from('<I',raw,q)[0]
        if n>4096 or q+4+n>e: break
        try: txt=raw[q+4:q+4+n].decode('utf-8')
        except Exception: break
        if not txt or not txt.isprintable(): break
        q+=4+n; tot+=n; k+=1
    return q,tot,k

for arch,const in (('client',65),('server',71)):
    raw=load(arch,18)
    p,b,_,_=dp_walk(raw,f'{arch}18',14,len(raw)-8,1567)
    rows=[(x[0],x[1]) for x in b]
    ok=0; ks=collections.Counter(); bad=[]
    for i,(s,e) in enumerate(rows):
        q,tot,k=strs(raw,s,e)
        if e-s==tot+const and k in (2,4): ok+=1; ks[k]+=1
        else: bad.append((i,e-s,tot,k))
    print(f't18 {arch}: rowlen==sum(text)+{const} ok {ok}/1567 k-dist {dict(ks)} bad {bad[:5]}')
    # tail structure after strings
    tail=collections.Counter()
    for s,e in rows:
        q,tot,k=strs(raw,s,e)
        tail[(e-q)]+=1
    print('   tail bytes after strings:', tail.most_common(6))
