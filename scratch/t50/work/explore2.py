import hashlib,os,pathlib,runpy,struct,sys
from collections import Counter,defaultdict
ROOT=pathlib.Path(r'D:\tmp2b\fm24-db'); sys.path.append(r'D:\tmp2b\fm24\tools\python')
import zstandard as z
codec=runpy.run_path(r'D:\tmp2b\fm24\scripts\modding_read_dbdat.py')
DB=pathlib.Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
P={}
for side in ('client','server'):
    db=(DB/f'{side}_db.dat').read_bytes(); lay=codec['_archive_layout'](db); base=lay['data_base']
    es={(x['path'].split('/')[-1]):x for x in lay['entries']}
    for name in ('table_9.dat','table_extra_9.dat','table_10.dat'):
        e=es[name]; lo=base+e['offset']
        s=z.ZstdDecompressor().decompressobj(); P[side,name]=s.decompress(db[lo:lo+e['packed_size']])
def cand(b,i):
    out=[]; s=0
    needle=struct.pack('<I',i)
    while True:
        p=b.find(needle,s)
        if p<0: break
        s=p+1
        if p+12<=len(b):
            c,d=struct.unpack_from('<II',b,p+4)
            if c==d and b[p+12]==0: out.append((p,c))
    return out
for side,name in [('client','table_9.dat'),('server','table_9.dat'),('client','table_extra_9.dat'),('server','table_extra_9.dat')]:
    b=P[side,name]; print('='*72); print(side,name,len(b))
    for i in list(range(0,4))+[250]:
        print('  ord',i,'candidates',cand(b,i)[:6],'n=',len(cand(b,i)))
