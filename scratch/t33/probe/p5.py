import struct
def walk(body,n,tail=13,minL=8,maxL=400):
    pos=0;rows=[]
    for i in range(n):
        hit=None
        for L in range(minL,maxL+1):
            t=pos+L-tail
            if t<pos or t+tail>len(body): break
            if tail==13:
                r,d1,d2=struct.unpack_from("<III",body,t)
                if r==i and d1==d2 and body[t+12]==0: hit=L;break
            else:
                a,b=struct.unpack_from("<II",body,t)
                if a==b and body[t+8]==0: hit=L;break
        if hit is None: return None,pos,i
        rows.append((pos,hit)); pos+=hit
    return rows,pos,n
for tid in (12,45,48,59):
    raw=open(f"scratch/t33/probe/t{tid}.bin","rb").read()
    n=struct.unpack_from("<I",raw,8)[0]; body=raw[14:len(raw)-8]
    for tail in (13,9):
        rows,end,idx=walk(body,n,tail)
        ok = rows is not None and end==len(body)
        print(tid,"tail",tail,"ok",ok,"stopped_row",idx,"pos",end,"bodylen",len(body))
        if ok:
            ls=[r[1] for r in rows]
            print("   len min/max",min(ls),max(ls),"sum",sum(ls))
