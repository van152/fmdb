import os,pathlib,runpy,struct,sys
ROOT=pathlib.Path(r'D:\tmp2b\fm24-db'); sys.path.append(r'D:\tmp2b\fm24\tools\python')
import zstandard as z
codec=runpy.run_path(r'D:\tmp2b\fm24\scripts\modding_read_dbdat.py')
DB=pathlib.Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
P={}
for side in ('client','server'):
    db=(DB/f'{side}_db.dat').read_bytes(); lay=codec['_archive_layout'](db); base=lay['data_base']
    es={(x['path'].split('/')[-1]):x for x in lay['entries']}
    e=es['table_extra_9.dat']; P[side]=z.ZstdDecompressor().decompressobj().decompress(db[base+e['offset']:base+e['offset']+e['packed_size']])
def isascii(b,lo,n): return 2<=n<=80 and lo+n<=len(b) and all(32<=x<127 for x in b[lo:lo+n])
for side in ('client','server'):
    b=P[side]; starts=[]
    for p in range(0,len(b)-8):
        idx,n=struct.unpack_from('<II',b,p)
        if idx<=260 and isascii(b,p+8,n): starts.append((p,idx,n,b[p+8:p+8+n].decode()))
    print('='*60); print(side,'pattern u32idx+u32len+ascii starts:',len(starts))
    print('  first 6',starts[:6])
