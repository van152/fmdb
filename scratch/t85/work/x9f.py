import sys,struct
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
for arch,size in (('client',83927),('server',105228)):
    raw=C.payload(arch,f'{arch}_db/table_extra_9.dat',size)
    hits=[]
    for i in range(12,len(raw)-8):
        o,l=struct.unpack_from('<II',raw,i)
        if 0<l<80 and all(32<=b<127 for b in raw[i+8:i+8+l]):
            hits.append((i,o,l))
    print('==',arch,'name-ish hits',len(hits),'first 12:',hits[:12])
