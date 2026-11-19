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
        e=es[name]; lo=base+e['offset']
        P[side,name]=z.ZstdDecompressor().decompressobj().decompress(db[lo:lo+e['packed_size']])
print("t10 tails for comparison")
for side in ('client','server'):
    b=P[side,'table_10.dat']; print(' ',side,len(b),'tail16',b[-16:].hex())
for side,name in [('client','table_9.dat'),('server','table_9.dat'),('client','table_extra_9.dat'),('server','table_extra_9.dat')]:
    b=P[side,name]; print('='*60); print(side,name,'len',len(b),'tail16',b[-16:].hex())
    # for 13B identity (a,x,x,m): census per ordinal over whole payload
    n=struct.unpack_from('<I',b,8)[0]
    per={}
    for p in range(13,len(b)-12):
        a,c,d=struct.unpack_from('<III',b,p)
        if a==c==d and a<=300 and a not in per:
            pass
    # collect
    hits=[]
    for p in range(13,len(b)-12):
        a,c,d=struct.unpack_from('<III',b,p)
        if c==d and a<=300 and b[p+12]==0:
            hits.append((a,p,c))
    cnt=Counter(h[0] for h in hits)
    print(' ordinals with candidates:',len(cnt),'histogram of candidate-counts:',Counter(cnt.values()))
    missing=[i for i in range(n) if i not in cnt]
    print(' missing ordinals count',len(missing),'first10',missing[:10])
