import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def lang6(raw):
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; out=[]
    for _ in range(cnt):
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4
        f=[]
        for _f in range(6):
            if raw[pos]==0xFF: pos+=1
            L=struct.unpack_from('<I',raw,pos)[0]
            f.append(raw[pos+4:pos+4+L]); pos+=4+L
        pos+=3
        out.append((uid,f))
    return out,pos

for nm in ('8_25.dat','15_0.dat','11_0.dat'):
    raw=lib.load_member('lang_update',nm)
    recs,pos=lang6(raw)
    print(f'== {nm} cnt={len(recs)} end={pos} len={len(raw)}')
    for r in recs[:5]: print('  ',r[0],[s.decode('utf-8','replace') for s in r[1]])

raw25=K['load_payload'](lib.CODEC,'client','25')
print('\ncomp table_25 rows 0..3 body bytes:')
for i in range(3):
    b=raw25[13+i*127:13+(i+1)*127]
    print(' ',i,b[:20].hex(' '),'u32@3',struct.unpack_from('<I',b,3)[0],'u32@4',struct.unpack_from('<I',b,4)[0])
