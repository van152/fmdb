import struct
def seqwalk(body,n,start_off=0,step=1,maxL=500):
    pos=start_off; got=0; lens=[]
    v=struct.unpack_from("<I",body,pos)[0]
    while got<n-1:
        want=v+step if step else got+1
        found=None
        for q in range(pos+8,min(pos+maxL,len(body)-3)):
            if struct.unpack_from("<I",body,q)[0]==want:
                found=q;break
        if found is None: return got,pos,lens
        lens.append(found-pos); pos=found; v=want; got+=1
    return got,pos,lens
for tid in (12,45,48,59):
    raw=open(f"scratch/t33/probe/t{tid}.bin","rb").read()
    n=struct.unpack_from("<I",raw,8)[0]; body=raw[14:len(raw)-8]
    g,p,l=seqwalk(body,n)
    print(tid,"inc-u32 walk rows",g+1,"of",n,"pos",p,"/",len(body),"len min/max/med",(min(l),max(l),sorted(l)[len(l)//2]) if l else None)
