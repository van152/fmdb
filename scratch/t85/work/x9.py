import sys,struct
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
for arch in ('client','server'):
    raw=C.payload(arch,f'{arch}_db/table_extra_9.dat',83927 if arch=='client' else 105228)
    print('==',arch,len(raw),'head',raw[:12].hex())
    print(' first 160:',raw[12:172].hex())
    print(' ascii:',raw[12:172].decode('latin-1').replace('\x00','.'))
