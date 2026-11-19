import os,pathlib,runpy,struct,sys
ROOT=pathlib.Path(r'D:\tmp2b\fm24-db'); sys.path.append(r'D:\tmp2b\fm24\tools\python')
import zstandard as z
codec=runpy.run_path(r'D:\tmp2b\fm24\scripts\modding_read_dbdat.py')
DB=pathlib.Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
db=(DB/'server_db.dat').read_bytes(); lay=codec['_archive_layout'](db); base=lay['data_base']
es={(x['path'].split('/')[-1]):x for x in lay['entries']}
e=es['table_9.dat']; b=z.ZstdDecompressor().decompressobj().decompress(db[base+e['offset']:base+e['offset']+e['packed_size']])
def cands(i):
    out=[]; needle=struct.pack('<I',i); p=b.find(needle,13)
    while p>=0:
        if p+13<=len(b):
            c,d=struct.unpack_from('<II',b,p+4)
            if c==d and b[p+12]==0: out.append((p,c))
        p=b.find(needle,p+1)
    return out
n=struct.unpack_from('<I',b,8)[0]; stop=len(b)-8
C={i:cands(i) for i in range(n)}
# enumerate distinct boundary sets
sols=set(); stack=[(0,13,-1,())]
import sys as _s
_s.setrecursionlimit(100000)
def rec(i,pos,last,acc):
    if i==n:
        if pos==stop: sols.add(acc)
        return
    for p,rid in C[i]:
        if p>=pos and p+13<=stop and rid>last and len(sols)<400:
            rec(i+1,p+13,rid,acc+((i,p,rid),))
rec(0,13,-1,())
print('distinct complete framings (mono ids):',len(sols))
sols=sorted(sols)
if len(sols)>1:
    base_set=sols[0]
    for k in range(1,min(6,len(sols))):
        diff=[(base_set[j],sols[k][j]) for j in range(n) if base_set[j]!=sols[k][j]]
        print(' variant',k,'diff rows',[(d[0][0],d[0][1],d[0][2],'->',d[1][1],d[1][2]) for d in diff])
