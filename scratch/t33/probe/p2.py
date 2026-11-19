import os, sys, struct, importlib.util
spec = importlib.util.spec_from_file_location("dump","scripts/fm24_dump.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
codec = m._reader()
for tid in (12,45,48,59):
    raw = m.load_payload(codec,"server",tid)
    open(f"scratch/t33/probe/t{tid}.bin","wb").write(raw)
    print("==",tid,"len",len(raw),"n",struct.unpack_from("<I",raw,8)[0])
    body=raw[14:14+240]
    for i in range(0,len(body),16):
        chunk=body[i:i+16]
        print(f"{14+i:5d} {chunk.hex(' '):<48} {''.join(chr(c) if 32<=c<127 else '.' for c in chunk)}")
