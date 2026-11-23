import sys,struct
sys.path.insert(0,'scripts')
import t38_multiframe as mf
c=mf._codec()
def payload(tid,arch): return mf.load_payload_mf(c,arch,tid)
def bounds(d,minlen=13):
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
        cand=[p for p in reach[k-1] if b[k]-p>=minlen]
        b[k-1]=min(cand)
    return b
def bodies(tid,arch):
    d=payload(tid,arch); b=bounds(d)
    out=[]
    for i in range(len(b)-1):
        r=d[b[i]:b[i+1]]
        out.append((r[0], r[1:-12], r[-12:]))
    return out
if __name__=='__main__':
    tid=int(sys.argv[1]); arch=sys.argv[2]; cnt=int(sys.argv[3]) if len(sys.argv)>3 else 3
    for i,(sel,body,ident) in enumerate(bodies(tid,arch)[:cnt]):
        print(f'row{i} sel={sel:02x} bodylen={len(body)} id={ident.hex()}')
        for j in range(0,len(body),16):
            ch=body[j:j+16]
            print(f'  {j:4d} {ch.hex(" "):<48} '+''.join(chr(x) if 32<=x<127 else '.' for x in ch))
