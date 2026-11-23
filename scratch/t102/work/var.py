import sys,struct
sys.path.insert(0,'scripts')
import t38_multiframe as mf
c=mf._codec()
def payload(tid,arch): return mf.load_payload_mf(c,arch,tid)
def bounds(d,minlen=14):
    n=struct.unpack_from('<I',d,8)[0]; end=len(d)-9
    reach=[{13}]
    for k in range(n):
        nxt=set()
        for p in reach[-1]:
            for e in range(p+minlen, end+1):
                if end-e < (n-k-1)*minlen: break
                if struct.unpack_from('<I',d,e-12)[0]==k and struct.unpack_from('<I',d,e-8)[0]==struct.unpack_from('<I',d,e-4)[0]:
                    nxt.add(e)
        reach.append(nxt)
    b=[None]*(n+1); b[n]=end
    for k in range(n,0,-1):
        c2=[p for p in reach[k-1] if b[k]-p>=minlen]
        b[k-1]=min(c2)
    return d,b
def strings(body):
    out=[]
    for i in range(0,max(0,len(body)-4)):
        L=struct.unpack_from('<I',body,i)[0]
        if 0<L<=64 and i+4+L<=len(body):
            s=body[i+4:i+4+L]
            if all(32<=x<127 for x in s):
                out.append((i,L,s.decode()))
    return out
if __name__=='__main__':
    tid=int(sys.argv[1]); arch=sys.argv[2]
    d,b=bounds(payload(tid,arch))
    n=len(b)-1
    for r in range(min(n,8)):
        body=d[b[r]+1:b[r+1]-12]
        print(f'row{r} bodylen={len(body)} strings={strings(body)}')
