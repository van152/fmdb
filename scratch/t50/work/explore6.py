import os,pathlib,runpy,struct,sys
from collections import Counter
ROOT=pathlib.Path(r'D:\tmp2b\fm24-db'); sys.path.append(r'D:\tmp2b\fm24\tools\python')
import zstandard as z
codec=runpy.run_path(r'D:\tmp2b\fm24\scripts\modding_read_dbdat.py')
DB=pathlib.Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
P={}
for side in ('client','server'):
    db=(DB/f'{side}_db.dat').read_bytes(); lay=codec['_archive_layout'](db); base=lay['data_base']
    es={(x['path'].split('/')[-1]):x for x in lay['entries']}
    for name in ('table_9.dat','table_extra_9.dat','table_10.dat'):
        e=es.get(name)
        if e: P[side,name]=z.ZstdDecompressor().decompressobj().decompress(db[base+e['offset']:base+e['offset']+e['packed_size']])
def cands(b,i,lo=13):
    out=[]; needle=struct.pack('<I',i); p=b.find(needle,lo)
    while p>=0:
        if p+13<=len(b):
            c,d=struct.unpack_from('<II',b,p+4)
            if c==d and b[p+12]==0 and c!=0: out.append((p,c))
        p=b.find(needle,p+1)
    return out
res={}
for side,name in [('client','table_9.dat'),('server','table_9.dat')]:
    b=P[side,name]; n=struct.unpack_from('<I',b,8)[0]; end=len(b)-8
    pos=13; rows=[]; 
    for i in range(n):
        cl=[x for x in cands(b,i,pos) if x[0]+13<=end]
        if not cl: rows.append(None); break
        r=cl[0]; rows.append((i,r[0],r[1],r[0]+13-pos,len(cl))); pos=r[0]+13
    res[side]=rows
    print(side,'rows',len(rows),'pos',pos,'end',end)
cid=[r[2] for r in res['client'] if r]; sid=[r[2] for r in res['server'] if r]
print('client ids',cid[:12],'...',cid[-4:])
print('server ids',sid[:12],'...',sid[-4:])
print('equal id lists:',cid==sid)
print('client strictly increasing:',all(x<y for x,y in zip(cid,cid[1:])),'unique',len(set(cid))==len(cid))
print('server strictly increasing:',all(x<y for x,y in zip(sid,sid[1:])),'unique',len(set(sid))==len(sid))
# order statistics: how many candidates exist for the chosen values, using full-payload scan
for side in ('client','server'):
    b=P[side,'table_9.dat']
    tot=Counter()
    for i in range(251):
        tot[len(cands(b,i,13))]+=1
    print(side,'full-scan candidate-count histogram',dict(sorted(tot.items())))
# t10 identity for reference: what do ids look like
for side in ('client','server'):
    b=P[side,'table_10.dat']; print(side,'t10 len',len(b))
