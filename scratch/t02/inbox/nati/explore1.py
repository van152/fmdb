import struct
d=open('client_db_t10.bin','rb').read()
body=d[14:len(d)-8]
N=len(body)
def u32(o): return struct.unpack_from('<I',body,o)[0]

# candidates: position off where u32(off)==k, u32(off+4)==u32(off+8), body[off+12]==0
cands={}
for off in range(0,N-12):
    a=u32(off)
    if a>300: continue
    b=u32(off+4); c=u32(off+8)
    if b==c and b!=0 and body[off+12]==0:
        cands.setdefault(a,[]).append((off,b))
for k in sorted(cands):
    print(k, cands[k][:6], len(cands[k]))
print('missing k:', [k for k in range(251) if k not in cands][:20])
