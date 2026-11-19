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
def strs(b):
    out=[]
    for p in range(0,len(b)-4):
        n=struct.unpack_from('<I',b,p)[0]
        if 2<=n<=80 and p+4+n<=len(b):
            s=b[p+4:p+4+n]
            if all(32<=x<127 for x in s) and sum(c in b'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ' for x in s for c in [x])>=max(2,n//2):
                out.append((p,n,s.decode()))
    return out
for side in ('client','server'):
    b=P[side]; ss=strs(b)
    print(side,'len',len(b),'string candidates',len(ss))
    print('  first 12:',ss[:12])
    print('  last 5:',ss[-5:])
    # positions of first few, check deltas
    pos=[x[0] for x in ss]
    print('  first 20 positions',pos[:20])
