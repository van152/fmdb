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
# db_id from id block: at row body start, pattern db_id,FFFF,db_id,db_id (u32 x4)
club={}
for i,off,body in rows:
    a,b,c,d=struct.unpack_from('<IIII',body,0)
    if b==0xFFFFFFFF and a==c==d: club.setdefault(a,[]).append((i,off,body))
print('club rows with id-block db_id:',sum(len(v) for v in club.values()),'unique',len(club))

recs,end=lang6(lib.load_member('lang_update','8_3.dat'))
hit=0; miss=0; diffs=[]
for uid,f in recs:
    if uid not in club: miss+=1; continue
    i,off,body=club[uid][0]
    hit+=1
    if len(diffs)<10:
        # inline strings in body
        inline=[]
        p=0
        while p<len(body)-4 and len(inline)<3:
            L=struct.unpack_from('<I',body,p)[0]
            if 2<=L<=120 and p+4+L<=len(body):
                try: s=body[p+4:p+4+L].decode('utf-8')
                except Exception: p+=1; continue
                if any(ch.isalpha() for ch in s): inline.append(s); p+=4+L; continue
            p+=1
        diffs.append((uid, [x.decode('utf-8','replace') for x in f], inline[:2], i))
print(f'lang 8_3 uid found as club db_id: hit={hit} miss={miss}')
for d in diffs: print('  ',d)
