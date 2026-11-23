import sys,struct
sys.path.insert(0,'scripts')
import t38_multiframe as mf
c=mf._codec()
def payload(tid,arch): return mf.load_payload_mf(c,arch,tid)
def bounds(d,maxbody=1000):
    n=struct.unpack_from('<I',d,8)[0]; end=len(d)-9
    reach=[{13}]
    for k in range(n):
        nxt=set()
        for p in reach[-1]:
            for e in range(p+13, min(end,p+13+maxbody)+1):
                if end-e < (n-k-1)*13: break
                if struct.unpack_from('<I',d,e-12)[0]==k and struct.unpack_from('<I',d,e-8)[0]==struct.unpack_from('<I',d,e-4)[0]:
                    nxt.add(e)
        reach.append(nxt)
    # backtrack unique path preferring ... pick smallest
    b=[None]*(n+1); b[n]=end
    for k in range(n,0,-1):
        cands=[p for p in reach[k-1] if b[k]-p>=13]
        b[k-1]=min(cands)
    return b,n
def rows(tid,arch):
    d=payload(tid,arch); b,n=bounds(d)
    return d,[d[b[i]:b[i+1]] for i in range(n)]
if __name__=='__main__':
    tid=int(sys.argv[1]); arch=sys.argv[2]; cnt=int(sys.argv[3]) if len(sys.argv)>3 else 4
    d,rs=rows(tid,arch)
    for i,r in enumerate(rs[:cnt]):
        body=r[1:len(r)-13]
        print(f'row{i} len={len(r)} body={len(body)} sel={r[0]:02x}')
        for j in range(0,len(body),16):
            ch=body[j:j+16]
            print(f'  {j:4d} {ch.hex(" "):<48} '+''.join(chr(x) if 32<=x<127 else '.' for x in ch))
