import sys, struct
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')

def parse_lang(raw):
    cnt=struct.unpack_from('<I',raw,8)[0]; pos=12; recs=[]
    while len(recs)<cnt:
        uid=struct.unpack_from('<I',raw,pos)[0]; pos+=4
        flds=[]
        while True:
            b=raw[pos]
            if b==0xFF: pos+=1; continue
            if b==0x00 and raw[pos+1]!=0: pos+=3; break
            L=struct.unpack_from('<I',raw,pos)[0]
            flds.append(raw[pos+4:pos+4+L]); pos+=4+L
        recs.append((uid,flds))
    return recs,pos

# club main rows: uid at row+16 (per t02 club_v2: db_id at row+0? verify)
raw3=K['load_payload'](lib.CODEC,'client','3')
rows=list(K['walk_club_block'](raw3))
print('club rows',len(rows),'len',len(raw3))
# uid position: t71 fixture Liverpool uid=676, ordinal 460
o,off,body=rows[460]
print('row460 len',len(body), body[:48].hex(' '))
import re
print('names', [m.group() for m in re.finditer(rb'[\x20-\xff]{3,}', body)][:4])
for cand in range(0,24,4):
    print('  u32@',cand,struct.unpack_from('<I',body,cand)[0])
