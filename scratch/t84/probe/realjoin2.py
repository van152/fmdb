import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def lang_uid_fields(raw, nf, tr):
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; recs=[]
    for _ in range(cnt):
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4; f=[]
        for _f in range(nf):
            if raw[pos]==0xFF: pos+=1
            L=struct.unpack_from('<I',raw,pos)[0]
            f.append(raw[pos+4:pos+4+L].decode('utf-8')); pos+=4+L
        pos+=tr; recs.append((uid,f))
    return recs,pos

raw3=K['load_payload'](lib.CODEC,'client','3')
# calibrate: find Liverpool, dump bytes before the length prefix
nm=b'Liverpool'
i=raw3.find(struct.pack('<I',len(nm))+nm)
print('len-prefix at',i,'name at',i+4)
print('ctx',raw3[i-40:i+4].hex(' '))
for back in range(24,40,2):
    a,b,c,d=struct.unpack_from('<IIII',raw3,i-back)
    if b==0xFFFFFFFF and a==c==d:
        print('  idblock at -',back,'db_id',a); break
