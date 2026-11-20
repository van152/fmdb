import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
import struct, hashlib, collections

def lstr(raw,q,e):
    if q+4>e: return None
    n=struct.unpack_from('<I',raw,q)[0]
    if n>4096 or q+4+n>e: return None
    try: t=raw[q+4:q+4+n].decode('utf-8')
    except Exception: return None
    if not t or not t.isprintable(): return None
    return q+4+n, n, t

def t8(arch):
    raw=load(arch,8); H,F=14,len(raw)-8
    p=H; i=0; lens=[]
    while p<F:
        r=lstr(raw,p,F)
        if not r: return ('fail_lstr',i,p)
        q,n,t=r
        # name, then 30B suffix: 17 pre + 13 identity
        if q+30>F: return ('fail_short',i)
        o,u1,u2=struct.unpack_from('<III',raw,q+17)
        if not(o==i and u1==u2 and raw[q+29]==0): return ('fail_id',i,o)
        if struct.unpack_from('<I',raw,q)[0]!=i and struct.unpack_from('<I',raw,q+13)[0]!=i:
            pass
        lens.append(4+n+30); p=q+30; i+=1
    return dict(rows=i,closure=(p==F),lens=(min(lens),max(lens)),sha=hashlib.sha256(raw).hexdigest(),
                suffix_head=[raw[H+4+struct.unpack_from('<I',raw,H)[0]:H+4+struct.unpack_from('<I',raw,H)[0]+17].hex()])

for arch in ('client','server'):
    print('t8',arch,t8(arch))
