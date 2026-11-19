import os,pathlib,runpy,struct,sys
ROOT=pathlib.Path(r'D:\tmp2b\fm24-db'); sys.path.append(r'D:\tmp2b\fm24\tools\python')
import zstandard as z
codec=runpy.run_path(r'D:\tmp2b\fm24\scripts\modding_read_dbdat.py')
DB=pathlib.Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
P={}
for side in ('client','server'):
    db=(DB/f'{side}_db.dat').read_bytes(); lay=codec['_archive_layout'](db); base=lay['data_base']
    es={(x['path'].split('/')[-1]):x for x in lay['entries']}
    for name in ('table_9.dat','table_extra_9.dat','table_10.dat','table_25.dat'):
        e=es.get(name)
        if e: P[side,name]=z.ZstdDecompressor().decompressobj().decompress(db[base+e['offset']:base+e['offset']+e['packed_size']])
def cands(b,i,lo=13):
    out=[]
    needle=struct.pack('<I',i)
    p=b.find(needle,lo)
    while p>=0:
        if p+13<=len(b):
            c,d=struct.unpack_from('<II',b,p+4)
            if c==d and b[p+12]==0: out.append((p,c))
        p=b.find(needle,p+1)
    return out
for side,name in [('client','table_9.dat'),('server','table_9.dat')]:
    b=P[side,name]; n=struct.unpack_from('<I',b,8)[0]; end=len(b)-8
    print('='*60); print(side,name,'n',n,'end',end)
    pos=13; rows=[]; fail=None
    for i in range(n):
        cl=[x for x in cands(b,i,pos) if x[0]+13<=end]
        if not cl: fail=(i,'no candidate',pos); break
        p,rid=cl[0]
        rows.append((i,p,rid,p+13-pos,len(cl)))
        pos=p+13
    print(' rows',len(rows),'pos after',pos,'end',end,'fail',fail)
    if rows:
        print(' first3',rows[:3]); print(' last2',rows[-2:])
        print(' id seq first8',[r[2] for r in rows[:8]])
        print(' ambiguity counts first20',[r[4] for r in rows[:20]])
