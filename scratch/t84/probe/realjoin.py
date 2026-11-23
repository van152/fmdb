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

recs,end=lang_uid_fields(lib.load_member('lang_update','8_3.dat'),6,3)
print('8_3 recs',len(recs),'end',end)

raw3=K['load_payload'](lib.CODEC,'client','3')
hit=miss=wrong=0; ex=[]
for uid,f in recs:
    nm=f[0].encode('utf-8')
    pat=struct.pack('<I',len(nm))+nm
    i=raw3.find(pat)
    if i<0: miss+=1; continue
    # expected id-block immediately before the len: db_id@i-30
    if i>=30:
        a,b,c,d=struct.unpack_from('<IIII',raw3,i-30)
        if b==0xFFFFFFFF and a==c==d and a==uid: hit+=1; ex.append((uid,f[0],'OK'))
        else: wrong+=1; ex.append((uid,f[0],f'idblock={a},{b:#x}',))
    else: wrong+=1
print(f'club lang join: name-found & db_id==uid: {hit}; name-found wrong id: {wrong}; not found: {miss}')
for e in ex[:6]: print('  ',e)
