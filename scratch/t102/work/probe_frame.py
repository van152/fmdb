import sys,struct
sys.path.insert(0,'scripts')
import t38_multiframe as mf
c=mf._codec()
T=[0,2,5,6,7,8,18,19,21,22,23,27,35,41,47,56]
def bounds(d):
    n=struct.unpack_from('<I',d,8)[0]; end=len(d)-9; b=[13]; p=13
    for k in range(n):
        f=None
        for e in range(p+2,end+1):
            if end-e < (n-k-1)*2: break
            if struct.unpack_from('<I',d,e-12)[0]==k and struct.unpack_from('<I',d,e-8)[0]==struct.unpack_from('<I',d,e-4)[0]:
                f=e;break
        if f is None: return None,k
        b.append(f);p=f
    if b[-1]!=end: return None,'tail'
    return b,n
for tid in T:
    for arch in ('server','client'):
        d=mf.load_payload_mf(c,arch,tid); r=bounds(d)
        if r[0] is None: print(tid,arch,'SEGFAIL',r[1]); continue
        b,n=r
        sel=set(d[b[i]] for i in range(n))
        foot=d[-9:]
        lastuid=struct.unpack_from('<I',d,b[-1]-8)[0]
        ok=foot[0:4]==b'\0\0\0\0' and foot[4]==1 and struct.unpack_from('<I',foot,5)[0]==lastuid
        segs=[b[i+1]-b[i] for i in range(n)]
        print(f'{tid:3d} {arch:6s} n={n:6d} body={sum(segs)-13*n:8d} sel={sorted(sel)} footer_ok={ok} foot={foot.hex()}')
