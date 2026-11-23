import struct
def walk(body,n,tail=13,markers=(0,0x0c),minL=13,maxL=600):
    pos=0;rows=[]
    for i in range(n):
        hit=None
        for L in range(minL,maxL+1):
            t=pos+L-tail
            if t<pos: continue
            if t+tail>len(body): break
            r,d1,d2=struct.unpack_from("<III",body,t)
            if r==i and d1==d2 and body[t+12] in markers: hit=L;break
        if hit is None: raise SystemExit(f"stuck {i}")
        rows.append(body[pos:pos+hit]); pos+=hit
    return rows
for tid in (45,48):
    raw=open(f"scratch/t33/probe/t{tid}.bin","rb").read()
    n=struct.unpack_from("<I",raw,8)[0]
    rows=walk(raw[14:len(raw)-8],n)
    print("==",tid,"rows",len(rows),"lens",min(len(r) for r in rows),max(len(r) for r in rows))
    for r in rows[:6]:
        print(f"  {len(r):3d} {r.hex(' ')}")
        print(f"      {''.join(chr(c) if 32<=c<127 else '.' for c in r)}")
