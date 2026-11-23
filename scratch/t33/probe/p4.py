import struct, collections
tests={12:[0x4de,0x436ad],45:[0x076c0001],48:[0x13db92],59:[0x23,0x77]}
for tid,cands in tests.items():
    raw=open(f"scratch/t33/probe/t{tid}.bin","rb").read()
    n=struct.unpack_from("<I",raw,8)[0]
    body=raw[14:len(raw)-8]
    print("==",tid,"n",n)
    for v in cands:
        pat=struct.pack("<I",v)
        pos=[];i=body.find(pat)
        while i>=0:
            pos.append(i); i=body.find(pat,i+1)
        gaps=collections.Counter(b-a for a,b in zip(pos,pos[1:]))
        print(f"  u32 {v:#x} count={len(pos)} first={pos[:5]} gaps={gaps.most_common(5)}")
