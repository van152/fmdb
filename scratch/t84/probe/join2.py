import sys, struct, re
sys.path.insert(0,'scratch/t84/probe')
import lib
K=lib.K
sys.stdout.reconfigure(encoding='utf-8', errors='backslashreplace')
raw3=K['load_payload'](lib.CODEC,'client','3')
rows=list(K['walk_club_block'](raw3))
targets=[b'Atl\xc3\xa9tico Petr\xc3\xb3leos de Luanda', b'Pyunik Yerevan', b'Liverpool']
for t in targets:
    for i,off,body in rows:
        if body.find(t)>=0:
            print(t.decode(), 'ordinal',i,'db_id@0',struct.unpack_from('<I',body,0)[0])
            print('   body head', body[:40].hex(' '))
            break
