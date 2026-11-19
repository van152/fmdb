import struct
for tid in (12,48):
    raw=open(f"scratch/t33/probe/t{tid}.bin","rb").read()
    n=struct.unpack_from("<I",raw,8)[0]; body=raw[14:len(raw)-8]
    print("==",tid,len(body))
    # find all positions p where u32 body[p]==0 (ordinal 0) and next two u32 equal and body[p+12] in (0,0x0c)
    hits=[]
    for p in range(0,len(body)-13):
        if body[p:p+4]!=b'\0\0\0\0': continue
        d1,d2=struct.unpack_from("<II",body,p+4)
        if d1==d2 and body[p+12] in (0,0x0c):
            hits.append((p,d1))
            if len(hits)>5: break
    print(" ordinal0 hits:",hits[:6])
    # ordinal 1
    hits=[]
    for p in range(0,len(body)-13):
        if struct.unpack_from("<I",body,p)[0]!=1: continue
        d1,d2=struct.unpack_from("<II",body,p+4)
        if d1==d2 and body[p+12] in (0,0x0c):
            hits.append((p,d1))
            if len(hits)>5: break
    print(" ordinal1 hits:",hits[:6])
