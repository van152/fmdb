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
for side in ('client','server'):
    b=P[side]; n=struct.unpack_from('<I',b,8)[0]; stop=len(b)-8
    C={i:cands(b,i) for i in range(n)}
    print('='*70); print(side,'len',len(b),'stop',stop,'footer last4',struct.unpack_from('<I',b,len(b)-4)[0])
    # state: (pos,lastid) -> count
    states={(13,-1):1}
    for i in range(n):
        nxt={}
        for (pos,last),cnt in states.items():
            for p,rid in C[i]:
                if p>=pos and p+13<=stop and rid>last:
                    k=(p+13,rid); nxt[k]=nxt.get(k,0)+cnt
        states=nxt
        if len(states)!=1 and i<5: print('  layer',i,'states',len(states))
        if not states: print('  dead at',i); break
    print('  states after all rows',len(states),'counts sum',sum(states.values()),'pos',sorted(set(k[0] for k in states))[:5])
