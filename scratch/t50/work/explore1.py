import hashlib,json,os,pathlib,runpy,struct,sys
from collections import Counter
ROOT=pathlib.Path(r'D:\tmp2b\fm24-db'); sys.path.append(r'D:\tmp2b\fm24\tools\python')
import zstandard as z
codec=runpy.run_path(r'D:\tmp2b\fm24\scripts\modding_read_dbdat.py')
DB=pathlib.Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
def H(b): return hashlib.sha256(b).hexdigest()
P={}
for side in ('client','server'):
    db=(DB/f'{side}_db.dat').read_bytes(); lay=codec['_archive_layout'](db); base=lay['data_base']
    es={(x['path'].split('/')[-1]):x for x in lay['entries']}
    for name in ('table_9.dat','table_extra_9.dat'):
        e=es[name]; lo=base+e['offset']
        s=z.ZstdDecompressor().decompressobj(); pl=s.decompress(db[lo:lo+e['packed_size']])
        P[side,name]=pl
# structural probes
for side,name in [('client','table_9.dat'),('server','table_9.dat'),('client','table_extra_9.dat'),('server','table_extra_9.dat')]:
    b=P[side,name]; n=struct.unpack_from('<I',b,8)[0]
    print('='*70); print(side,name,'len',len(b),'count',n)
    print(' head13',b[:13].hex(),' tail24',b[-24:].hex())
    # footer guess: last 9 bytes
    print(' last9',b[-9:].hex(),'u32@-9',struct.unpack_from('<I',b,len(b)-9)[0],'flag',b[-5],'maxid',struct.unpack_from('<I',b,len(b)-4)[0])
    # identity tail census: triple (i,i,i)+0 anywhere
    hits=[]
    for pos in range(0,len(b)-12):
        a,c,d=struct.unpack_from('<III',b,pos)
        if a==c==d and b[pos+12]==0 and a<300:
            hits.append((pos,a))
    print(' ident triples',len(hits),'first5',hits[:5],'last3',hits[-3:])
