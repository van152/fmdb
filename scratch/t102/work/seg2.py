import sys,struct
sys.path.insert(0,'scripts')
import t38_multiframe as mf
c=mf._codec()
def payload(tid,arch):
    return mf.load_payload_mf(c,arch,tid)
def bounds_back(d,window=1200):
    n=struct.unpack_from('<I',d,8)[0]; e=len(d)-9
    ends=[e]
    for k in range(n-1,-1,-1):
        found=None
        lo=max(13+k*2, e-window)
        for p in range(e,lo,-1):
            if struct.unpack_from('<I',d,p-12)[0]==k and struct.unpack_from('<I',d,p-8)[0]==struct.unpack_from('<I',d,p-4)[0]:
                found=p; break
        if found is None: return None,k
        ends.append(found); e=found
    ends.reverse()
    if ends[0]!=13: return None,'start %d'%ends[0]
    return ends,n
if __name__=='__main__':
    T=[0,2,5,6,7,8,18,19,21,22,23,27,35,41,47,56]
    for tid in T:
        for arch in ('server','client'):
            d=payload(tid,arch)
            r=bounds_back(d)
            if r[0] is None: print(tid,arch,'FAIL',r[1]); continue
            b,n=r; segs=[b[i+1]-b[i] for i in range(n)]
            print(f'{tid:3d} {arch:6s} n={n:6d} min={min(segs)} max={max(segs)} uniq={len(set(segs))}')
