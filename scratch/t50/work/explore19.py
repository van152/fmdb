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
    e=es['table_extra_9.dat']; P[side]=z.ZstdDecompressor().decompressobj().decompress(db[base+e['offset']:base+e['offset']+e['packed_size']])
def ok(b,p,i,maxln=200):
    if p+8>len(b): return None
    a,ln=struct.unpack_from('<II',b,p)
    if a!=i or ln>maxln or p+8+ln>len(b): return None
    if any(x<0x20 for x in b[p+8:p+8+ln]): return None
    return ln
def walk(b):
    n=struct.unpack_from('<I',b,8)[0]; starts=[12]; pos=12
    for i in range(1,n):
        for d in range(0,30000):
            q=pos+d
            if q>=len(b): break
            if ok(b,q,i) is not None: starts.append(q); pos=q; break
    return starts
for side in ('client','server'):
    b=P[side]; st=walk(b); ends=st[1:]+[len(b)]
    print('='*70); print(side,'len',len(b),'records',len(st))
    # ambiguity: for each ordinal, count candidates within [prev_start, end]
    amb=[]
    for k,i in enumerate(range(251)):
        lo=st[k]; hi=ends[k]
        cnt=0
        for d in range(lo,hi):
            if ok(b,d,i) is not None: cnt+=1
        amb.append((i,cnt,hi-lo))
    print('  amb hist (within record window)',Counter(a[1] for a in amb))
    print('  multi-candidate ords',[a for a in amb if a[1]>1][:10])
    # check trailer: bytes just before each next record start
    print('  rec lens hist',Counter(e-s for s,e in zip(st,ends)).most_common(8))
