import struct
d=open('client_db_t10.bin','rb').read()
body=d[14:len(d)-8]; N=len(body)
def u32(o): return struct.unpack_from('<I',body,o)[0]
cands={}
for off in range(0,N-12):
    a=u32(off)
    if a>250: continue
    b=u32(off+4)
    if b==u32(off+8) and 0<b<0xFFFFFFFF and body[off+12]==0:
        cands.setdefault(a,[]).append((off,b))
# pick monotone: for row0 pick candidate with smallest ID and off<60
R=[0]
pick=[]
for k in range(251):
    opts=[c for c in cands[k] if c[0]>=R[k]+13]  # identity must be at least 13 bytes into row
    if not opts: print("no cand",k); break
    # choose candidate whose +13 is < next row's candidate start
    c=min(opts, key=lambda t:(t[1],t[0]))
    pick.append(c)
    R.append(c[0]+13)
print('rows',len(R)-1,'end',R[-1],'/',N,'closure',R[-1]==N)
lens=[R[i+1]-R[i] for i in range(len(R)-1)]
print('len min/max',min(lens),max(lens),'distinct',len(set(lens)))
print('first 12 starts',R[:12])
print('first 12 lens',lens[:12])
# field sanity
bad=[]
for k in range(251):
    s=R[k]
    ngct=body[s]; ncti=u32(s+1); nrgi=u32(s+5); x9=u32(s+9); ncur=u32(s+13)
    nsod=body[s+17]; necf=body[s+18]; x19=u32(s+19); nygn=body[s+23]; c1=body[s+24]
    if not (ncti<=5): bad.append((k,'ncti',ncti))
print('ncti>5 count',len(bad),bad[:10])
vals={}
for k in range(251):
    s=R[k]; vals.setdefault('ngct',[]).append(body[s]); vals.setdefault('ncur',[]).append(u32(s+13))
    vals.setdefault('nsod',[]).append(body[s+17]); vals.setdefault('necf',[]).append(body[s+18])
    vals.setdefault('nygn',[]).append(body[s+23]); vals.setdefault('c1',[]).append(body[s+24])
for kk in vals:
    print(kk,'min',min(vals[kk]),'max',max(vals[kk]),'distinct',len(set(vals[kk])), sorted(set(vals[kk]))[:15])
