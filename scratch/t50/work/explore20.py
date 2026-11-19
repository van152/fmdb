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
    for name in ('table_9.dat',):
        e=es[name]; P[side]=z.ZstdDecompressor().decompressobj().decompress(db[base+e['offset']:base+e['offset']+e['packed_size']])
def ident_positions(b,i):
    out=[]; needle=struct.pack('<I',i); p=b.find(needle,13)
    while p>=0:
        if p+13<=len(b):
            c,d=struct.unpack_from('<II',b,p+4)
            if c==d and b[p+12]==0: out.append((p,c))
        p=b.find(needle,p+1)
    return out
for side in ('client','server'):
    b=P[side]; n=struct.unpack_from('<I',b,8)[0]; end=len(b)-8
    cands={i:ident_positions(b,i) for i in range(n)}
    # DP: reach[i] = dict pos->count ; rows 0..i-1 laid out ending at pos
    reach={13:1}
    layer=[dict(reach)]
    for i in range(n):
        nxt={}
        for pos,cnt in reach.items():
            for (p,rid) in cands[i]:
                if p>=pos and p+13<=end:
                    nxt[p+13]=nxt.get(p+13,0)+cnt
        reach=nxt; layer.append(dict(reach))
        if not reach: print(side,'DEAD at row',i); break
    print('='*60); print(side,'complete walks ending at',end,':',reach.get(end,0),' states at final layer',len(reach))
    print('  layer widths first 8',[len(x) for x in layer[:8]],'max',max(len(x) for x in layer))
    print('  mid-layer sample',[len(x) for x in layer[60:70]])
