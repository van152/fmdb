import runpy, sys, struct
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
raw5 = dump['load_payload'](codec,'client',5)
raw5s = dump['load_payload'](codec,'server',5)
print('client 5 rows')
for i in range(7):
    r=raw5[14+i*34:14+(i+1)*34]
    print(i, r.hex())
    print('  u8 :', list(r))
print('server 5 rows stride 48')
for i in range(7):
    r=raw5s[14+i*48:14+(i+1)*48]
    print(i, r.hex())
print('server5 header',raw5s[:14].hex(),'footer',raw5s[-8:].hex())
print('server5 total',len(raw5s),' 13+7*48+9=',13+7*48+9,'14+7*48+8=',14+7*48+8)
raw19 = dump['load_payload'](codec,'client',19); raw19s=dump['load_payload'](codec,'server',19)
print('19 client',len(raw19),'13+28*45+9',13+28*45+9,'14+28*45+8',14+28*45+8)
print('19 server',len(raw19s),'28*46',(len(raw19s)-13-9)/28, (len(raw19s)-14-8)/28)
for i in (0,2,3):
    print(' s19',i,raw19s[14+i*46:14+(i+1)*46].hex() if False else '')
print(' s19 assume 13+ n*46 +9:',(len(raw19s)-22)/28)
