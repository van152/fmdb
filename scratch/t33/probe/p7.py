import struct
def walk(body,n,base=1,tail=13,kmax=40,minL=20):
    pos=0;rows=[]
    for i in range(n):
        hit=None
        for k in range(0,kmax):
            L=minL+5*k
            t=pos+L-tail
            if t<pos or t+tail>len(body): break
            if tail==13:
                r,d1,d2=struct.unpack_from("<III",body,t)
                if r==i+base and d1==d2 and body[t+12]==0: hit=L;break
            else:
                a,b=struct.unpack_from("<II",body,t)
                if a==b and body[t+8]==0: hit=L;break
        if hit is None: return None,pos,i
        rows.append((pos,hit)); pos+=hit
    return rows,pos,n
for tid in (12,45,48,59):
    raw=open(f"scratch/t33/probe/t{tid}.bin","rb").read()
    n=struct.unpack_from("<I",raw,8)[0]; body=raw[14:len(raw)-8]
    for base in (0,1):
        for tail in (13,9):
            for minL in (20,41):
                rows,end,idx=walk(body,n,base,tail,40,minL)
                ok = rows is not None and end==len(body)
                if rows is not None:
                    print(tid,"base",base,"tail",tail,"minL",minL,"rows",idx,"end",end,"/",len(body),"FULL" if ok else "")
