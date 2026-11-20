import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def lang6(raw):
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; out=[]
    for _ in range(cnt):
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4; f=[]
        while True:
            b=raw[pos]
            if b==0xFF: pos+=1; continue
            if b==0x00 and raw[pos+1]!=0: pos+=3; break
            L=struct.unpack_from('<I',raw,pos)[0]
            f.append(raw[pos+4:pos+4+L]); pos+=4+L
        out.append((uid,f))
    return out,pos

raw3=K['load_payload'](lib.CODEC,'client','3')
rows=list(K['walk_club_block'](raw3))
# build map: inline full name -> (row, db_id from id-block scan)
names={}
for i,off,body in rows:
    for back in range(4,60):
        p=off-back
        if p<0: break
        a,b,c,d=struct.unpack_from('<IIII',raw3,p)
        if b==0xFFFFFFFF and a==c==d and 0<a<10**7:
            L=struct.unpack_from('<I',body,26)[0] if len(body)>30 else 0
            if 2<=L<=120 and 30+L<=len(body):
                try: s=body[30:30+L].decode('utf-8')
                except Exception: s=None
                if s and any(ch.isalpha() for ch in s): names.setdefault(s,(i,a))
            break
print('club inline names captured:',len(names))

recs,end=lang6(lib.load_member('lang_update','8_3.dat'))
print('lang 8_3 recs',len(recs),'end',end,'target',282975)
hit=0; idhit=0; miss=0; ex=[]
for uid,f in recs:
    nm=f[0].decode('utf-8','replace')
    if nm in names:
        hit+=1
        i,did=names[nm]
        if did==uid: idhit+=1
        if len(ex)<6: ex.append((uid,did,nm[:30],i))
    else: miss+=1
print(f'name match: hit={hit} miss={miss}; uid==db_id among hits: {idhit}')
for e in ex: print('  uid',e[0],'db_id',e[1],repr(e[2]),'row',e[3])
