import sys,struct
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
raw=C.payload('client','client_db/name_table_extra_1.dat',8713837)
print('head',raw[:14].hex(' '),'len',len(raw))
# find England
p=0
while True:
    p=raw.find(b'England',p)
    if p<0: break
    print('England at',p,'ctx',raw[p-24:p+40].hex(' '))
    print('   ascii',raw[p-24:p+40].decode('latin-1').replace('\x00','.'))
    p+=1
