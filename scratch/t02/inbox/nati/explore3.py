import struct
d=open('client_db_t10.bin','rb').read()
body=d[14:len(d)-8]; N=len(body)
def u32(o): return struct.unpack_from('<I',body,o)[0]
# starts via identity-block-at-end: find all off where u32(off)=k, u32(off+4)==u32(off+8), body[off+12]==0
cands={}
for off in range(0,N-12):
    a=u32(off)
    if a>250: continue
    b=u32(off+4)
    if b==u32(off+8) and 0<b<0xFFFFFFFF and body[off+12]==0:
        cands.setdefault(a,[]).append(off)
R=[0]
for k in range(251):
    opts=[o for o in cands[k] if o>=R[k]+13]
    if not opts: print('no',k); break
    # prefer candidate at end such that next row starts exactly
    R.append(min(opts)+13)
lens=[R[i+1]-R[i] for i in range(251)]
print('closure', R[-1]==N, R[-1], N)
# verify identity block at row end
ok=all(u32(R[k]+lens[k]-13)==k and u32(R[k]+lens[k]-9)==u32(R[k]+lens[k]-5) for k in range(251))
print('identity-at-end holds:', ok)
print(' k  len b24 b25 b26 b27 b28 b29 | head-tail content len')
for k in list(range(6))+[46,47,55,60,61,121,126,143,170,197,198,213,216,247,250]:
    s=R[k]; L=lens[k]; c=L-25-13
    print(f'{k:4d} {L:5d} {body[s+24]:3d} {body[s+25]:3d} {body[s+26]:3d} {body[s+27]:3d} {body[s+28]:3d} {body[s+29]:3d} | seg={c:4d}')
