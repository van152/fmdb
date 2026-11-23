import sys,struct
sys.path.insert(0,'scripts')
import t38_multiframe as mf
c=mf._codec()
T=[0,2,5,6,7,8,18,19,21,22,23,27,35,41,47,56]
def parse(d, maxbody=900):
    n=struct.unpack_from('<I',d,8)[0]; end=len(d)-9
    reach=[{13}]
    for k in range(n):
        nxt=set()
        for p in reach[-1]:
            for e in range(p+13, min(end, p+13+maxbody)+1):
                if end-e < (n-k-1)*13: break
                if struct.unpack_from('<I',d,e-12)[0]==k and struct.unpack_from('<I',d,e-8)[0]==struct.unpack_from('<I',d,e-4)[0]:
                    nxt.add(e)
        reach.append(nxt)
        if not nxt: return None,k,len(reach[-2])
    return reach,n,None
for tid in T:
    for arch in ('server','client'):
        d=mf.load_payload_mf(c,arch,tid)
        r=parse(d)
        if r[0] is None: print(tid,arch,'FAIL row',r[1],'cands',r[2]); continue
        reach,n,_=r
        amb=[(k,len(reach[k])) for k in range(n+1) if len(reach[k])!=1]
        ok = (len(d)-9) in reach[n]
        print(f'{tid:3d} {arch:6s} n={n:6d} close={ok} amb_positions={len(amb)} maxamb={max([a[1] for a in amb],default=1)}')
