import sys,struct,re
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
def walk(raw, hdr=12):
    p=hdr; n=0; blocks=[]
    while p+8<=len(raw):
        o,l=struct.unpack_from('<II',raw,p)
        if o!=n or not (0<l<200): break
        txt=raw[p+8:p+8+l]
        if not all(32<=b<127 for b in txt): break
        blocks.append((p,o,l,txt.decode('latin-1')))
        p=p+8+l; n+=1
    return blocks,p
for arch,size in (('client',83927),('server',105228)):
    raw=C.payload(arch,f'{arch}_db/table_extra_9.dat',size)
    b,end=walk(raw)
    print(arch,'blocks',len(b),'ended at',end,'of',len(raw))
    for i in (0,1,2,55,139):
        if i<len(b): print('  ',b[i][1],repr(b[i][3]),'at',b[i][0])
