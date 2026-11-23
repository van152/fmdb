import sys,struct
sys.path.insert(0,'scripts')
import t38_multiframe as mf
c=mf._codec()
def rows(tid,arch):
    d=mf.load_payload_mf(c,arch,tid); n=struct.unpack_from('<I',d,8)[0]; return d,n
def seg(tid,arch):
    d,n=rows(tid,arch); end=len(d)-9; b=[13]; p=13
    for k in range(n):
        for e in range(p+2,end+1):
            if end-e < (n-k-1)*2: break
            if struct.unpack_from('<I',d,e-12)[0]==k and struct.unpack_from('<I',d,e-8)[0]==struct.unpack_from('<I',d,e-4)[0]:
                b.append(e); p=e; break
        else: raise SystemExit('fail')
    return d,b
def show(tid,arch,idx):
    d,b=seg(tid,arch)
    for r in idx:
        o,s=b[r],b[r+1]-b[r]
        row=d[o:o+s]
        print(f'-- t{tid} {arch} row{r} len{s}')
        for i in range(0,s,8):
            chunk=row[i:i+8]
            printable=''.join(chr(x) if 32<=x<127 else '.' for x in chunk)
            print(f'   {i:4d} {chunk.hex(" "):<24} {printable}')
if __name__=='__main__':
    tid=int(sys.argv[1]); arch=sys.argv[2]; idx=[int(x) for x in sys.argv[3].split(',')]
    show(tid,arch,idx)
