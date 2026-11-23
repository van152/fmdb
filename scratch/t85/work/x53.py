import sys,struct
sys.stdout.reconfigure(encoding='utf-8')
raw=open('scratch/data/lang_update_db.dat','rb').read()
print('len',len(raw),'head',raw[:32].hex(' '))
for n in (b'Algeria',b'England',b'Alg\xc3\xa9rie',b'A\x00l\x00g'):
    print(n,raw.count(n))
print('ascii sample',raw[:200].decode('latin-1').replace('\x00','.')[:200])
