import sys; sys.path.insert(0,'scratch/t74')
from _probe import load
from _dp import dp_walk
import struct, collections

def rows_of(arch,tid,n):
    raw=load(arch,tid)
    p,b,_,_ = dp_walk(raw,f'{arch}{tid}',14,len(raw)-8,n)
    return raw, [(x[0],x[1]) for x in b]

def check_id(raw,rows,n):
    ok_ord = 0; bad=[]
    for i,(s,e) in enumerate(rows):
        o,u1,u2=struct.unpack_from('<III',raw,e-13)
        mk=raw[e-1]
        if o==i and u1==u2 and u1>0 and mk==0: ok_ord+=1
        else: bad.append((i,o,u1,u2,mk))
    return ok_ord, bad

# ---- t18: hypothesis mid = fixed len (client 44 / server 50)
for arch,midlen in (('client',44),('server',50)):
    raw=load(arch,18); end=len(raw)-8
    pos=14; ok=True; rows=[]
    for i in range(1567):
        nl1=struct.unpack_from('<I',raw,pos)[0]
        q=pos+4+nl1
        nl2=struct.unpack_from('<I',raw,q)[0]
        q+=4+nl2
        q+=midlen
        q+=13
        rows.append((pos,q)); pos=q
        if q>end: ok=False; break
    good,nb = check_id(raw,rows,1567)
    print(f't18 {arch} mid={midlen}: closure {pos==end} rows {len(rows)} identity_ok {good}/1567', nb[:2])
    if pos==end:
        ords=[struct.unpack_from('<I',raw,e-13)[0] for s,e in rows]
        uids=[struct.unpack_from('<I',raw,e-9)[0] for s,e in rows]
        print('   ord==0..n-1',ords==list(range(1567)),'uid increasing',all(uids[i]<uids[i+1] for i in range(1566)))
        print('   mid head/tail sample', raw[rows[0][0]:rows[0][1]][28:28+midlen].hex(' '))

# ---- t7: mid = 30 head + u32 count + count*12 + (server +7) + 5 tail
for arch,extra in (('client',0),('server',7)):
    raw=load(arch,7); end=len(raw)-8
    pos=14; rows=[]; ok=True
    for i in range(208):
        nl=struct.unpack_from('<I',raw,pos)[0]
        q=pos+4+nl+6
        ul=struct.unpack_from('<I',raw,q)[0]
        q+=4+ul
        q+=30
        c=struct.unpack_from('<I',raw,q)[0]
        q+=4+12*c
        q+=extra
        q+=5+13
        rows.append((pos,q)); pos=q
        if q>end or c>500: ok=False; break
    good,nb=check_id(raw,rows,208)
    print(f't7 {arch} extra={extra}: closure {pos==end} rows {len(rows)} identity_ok {good}/208', nb[:2])
    if pos==end:
        print('   counts', [struct.unpack_from('<I',raw,s+4+struct.unpack_from("<I",raw,s)[0]+6+4+struct.unpack_from("<I",raw,s+4+struct.unpack_from("<I",raw,s)[0]+6)[0]+30)[0] for s,e in rows[:8]])

# ---- t8: name + 30B suffix where suffix = 17 pre + 13 identity
for arch in ('client','server'):
    raw=load(arch,8); end=len(raw)-8
    pos=14; rows=[]
    for i in range(126):
        nl=struct.unpack_from('<I',raw,pos)[0]
        q=pos+4+nl+30
        rows.append((pos,q)); pos=q
    good,nb=check_id(raw,rows,126)
    print(f't8 {arch}: closure {pos==end} identity_ok {good}/126', nb[:3])
    # pre-area 17 bytes: u32@17 of suffix
    vals=[struct.unpack_from('<I',raw,s+4+struct.unpack_from('<I',raw,s)[0]+17)[0] for s,e in rows]
    print('   suffix+17 u32 == 0..125?', vals==list(range(126)), 'first', vals[:5])
