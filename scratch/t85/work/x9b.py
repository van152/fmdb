import sys,struct,re
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
for arch,size in (('client',83927),('server',105228)):
    raw=C.payload(arch,f'{arch}_db/table_extra_9.dat',size)
    print('====',arch,'len',len(raw),'header12',raw[:12].hex())
    # collect ascii runs >=4
    runs=[(m.start(),m.group()) for m in re.finditer(rb'[ -~]{4,}',raw)]
    print(' ascii runs',len(runs),'first 25:')
    for o,s in runs[:25]: print('   ',o,s.decode())
