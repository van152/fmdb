import struct
def walk(body,n,minL=13,maxL=600):
    pos=0;rows=[]
    for i in range(n):
        hit=None
        for L in range(minL,maxL+1):
            t=pos+L-13
            if t<pos: continue
            if t+13>len(body): break
            r,d1,d2=struct.unpack_from("<III",body,t)
            if r==i and d1==d2 and body[t+12] in (0,0x0c): hit=L;break
        if hit is None: raise SystemExit(f"stuck {i}")
        rows.append(body[pos:pos+hit]); pos+=hit
    return rows
for tid in (12,45,48,59):
    raw=open(f"scratch/t33/probe/t{tid}.bin","rb").read()
    n=struct.unpack_from("<I",raw,8)[0]
    rows=walk(raw[14:len(raw)-8],n)
    # test duplication: u32 at even offsets vs +4
    print("==",tid,"n",len(rows),"minlen",min(map(len,rows)))
    same=[0]*8; tot=[0]*8
    for r in rows:
        for k in range(0,min(28,len(r)-8),4):
            if k+8>len(r): break
            a,b=struct.unpack_from("<II",r,k)
            i=k//4
            if i<8:
                tot[i]+=1; same[i]+= (a==b)
    print("  dup pairs rate", [f"{k}:{same[k]/max(1,tot[k]):.3f}" for k in range(8) if tot[k]])
