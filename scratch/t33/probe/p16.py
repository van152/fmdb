import struct
for tid,st,rowstart in ((39,42,14),(58,45,14),(73,23,14)):
    raw=open(f"scratch/t33/probe/t{tid}.bin","rb").read()
    print("==",tid,"len",len(raw),"n",struct.unpack_from("<I",raw,8)[0])
    n=struct.unpack_from("<I",raw,8)[0]
    for i in range(min(n,10)):
        r=raw[rowstart+i*st:rowstart+(i+1)*st]
        print(f"  row{i} {r.hex(' ')}")
