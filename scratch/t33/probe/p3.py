import struct, collections
for tid in (12,45,48,59):
    raw=open(f"scratch/t33/probe/t{tid}.bin","rb").read()
    n=struct.unpack_from("<I",raw,8)[0]
    body=raw[14:len(raw)-8]
    print("==",tid,"payload",len(raw),"n",n,"body",len(body),"avg",round(len(body)/n,3))
    print("  head14:",raw[:14].hex(), "tail:",raw[-8:].hex())
    # try constant u32 at row start candidates: most common u32 value & its positions
    c=collections.Counter(struct.unpack_from("<I",body,i)[0] for i in range(0,len(body)-3))
    for v,k in c.most_common(4):
        if k>2:
            pos=[i for i in range(0,len(body)-3) if struct.unpack_from("<I",body,i)[0]==v]
            gaps=collections.Counter(b-a for a,b in zip(pos,pos[1:]))
            print(f"  u32={v:#x} count={k} first={pos[:6]} gaps={gaps.most_common(6)}")
