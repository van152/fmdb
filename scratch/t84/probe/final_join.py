import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def langf(raw,nf,tr):
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; recs=[]
    for _ in range(cnt):
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4; f=[]
        for _f in range(nf):
            if raw[pos]==0xFF: pos+=1
            L=struct.unpack_from('<I',raw,pos)[0]
            f.append(raw[pos+4:pos+4+L].decode('utf-8')); pos+=4+L
        pos+=tr; recs.append((uid,f))
    return recs

raw3=K['load_payload'](lib.CODEC,'client','3')
def idblock_before(pos):
    for back in range(24,40):
        p=pos-back
        if p<0: return None
        a,b,c,d=struct.unpack_from('<IIII',raw3,p)
        if b==0xFFFFFFFF and a==c==d and 0<a<2*10**6: return a
    return None

recs=langf(lib.load_member('lang_update','8_3.dat'),6,3)
hit=wrong=miss=0; ex=[]
for uid,f in recs:
    nm=f[0].encode('utf-8')
    i=raw3.find(struct.pack('<I',len(nm))+nm)
    if i<0: miss+=1; continue
    did=idblock_before(i)
    if did is None: miss+=1; continue
    if did==uid: hit+=1
    else:
        wrong+=1
        if len(ex)<5: ex.append((uid,did,f[0][:26]))
print(f'CLUB 8_3: exact-name found {hit+wrong}, db_id==lang uid {hit}, mismatch {wrong}, not-found {miss}')
for e in ex: print('   lang_uid',e[0],'row db_id',e[1],repr(e[2]))
