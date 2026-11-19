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
    e=es['table_9.dat']; P[side]=z.ZstdDecompressor().decompressobj().decompress(db[base+e['offset']:base+e['offset']+e['packed_size']])
def cands(b,i):
    out=[]; needle=struct.pack('<I',i); p=b.find(needle,13)
    while p>=0:
        if p+13<=len(b):
            c,d=struct.unpack_from('<II',b,p+4)
            if c==d and b[p+12]==0: out.append((p,c))
        p=b.find(needle,p+1)
    return out
def walk(b):
    n=struct.unpack_from('<I',b,8)[0]; stop=len(b)-8
    C={i:cands(b,i) for i in range(n)}
    states={(13,-1):1}
    parent=[]
    for i in range(n):
        nxt={}
        for (pos,last),cnt in states.items():
            for p,rid in C[i]:
                if p>=pos and p+13<=stop and rid>last:
                    nxt[(p+13,rid)]=nxt.get((p+13,rid),0)+cnt
        if len(nxt)!=1: print('  layer',i,'n',len(nxt))
        states=nxt
        parent.append(list(states))
    return parent
for side in ('client','server'):
    b=P[side]; print('='*60); print(side); w=walk(b); print(' final',w[-1])
