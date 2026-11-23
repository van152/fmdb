import sys, struct, re
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
raw=K['load_payload'](lib.CODEC,'client','3')
rows=list(K['walk_club_block'](raw))
for i,off,body in rows:
    if b'Petro' in body or b'petro' in body:
        print('club row',i,'off',off,'len',len(body), body[:60].hex(' '))
        print('   ', [m.group() for m in re.finditer(rb'[ -~\xc0-\xff]{4,}', body)][:6])
        if i>200: break
print('--- first 6 club names with uid')
for i,off,body in rows[:6]:
    uid=struct.unpack_from('<I',body,16)[0]
    print(i,'uid@16',uid, body[30:70])
