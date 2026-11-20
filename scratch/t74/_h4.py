import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections, json

H={}
def lstr(raw,q,e):
    n=struct.unpack_from('<I',raw,q)[0]
    if n>4096 or q+4+n>e: return None
    try: t=raw[q+4:q+4+n].decode('utf-8')
    except Exception: return None
    if not t or not t.isprintable(): return None
    return q+4+n,n

for arch in ('client','server'):
    raw=load(arch,8); F=len(raw)-8; p=14; lens=[]
    while p<F:
        q,n=lstr(raw,p,F); lens.append(4+n+30); p=q+30
    H[f'8_{arch}']=dict(collections.Counter(lens))
    raw=load(arch,7); F=len(raw)-8
    _,b,_,_=dp_walk(raw,f'{arch}7',14,F,208)
    H[f'7_{arch}']=dict(collections.Counter([x[1]-x[0] for x in b]))
    raw=load(arch,27); F=len(raw)-8; p=14; lens=[]
    while p<F:
        L=struct.unpack_from('<I',raw,p)[0]; e=p+4+L+95+13; lens.append(e-p); p=e
    H[f'27_{arch}']=dict(collections.Counter(lens))
    raw=load(arch,47); F=len(raw)-8
    pp,b,_,_=dp_walk(raw,f'{arch}47',14,F,2488)
    lens=[x[1]-x[0] for x in b]
    assert pp==1 and b[-1][1]==F and all((L-41)%5==0 for L in lens)
    H[f'47_{arch}']=dict(collections.Counter(lens))
    raw=load(arch,18); F=len(raw)-8
    _,b,_,_=dp_walk(raw,f'{arch}18',14,F,1567)
    H[f'18_{arch}']=dict(collections.Counter([x[1]-x[0] for x in b]))
json.dump(H,open('scratch/t74/_hists.json','w'))
print({k:(min(x),max(x),len(x),sum(x.values())) for k,x in H.items()})
