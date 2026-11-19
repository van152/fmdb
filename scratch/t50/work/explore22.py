import os,pathlib,runpy,struct,sys
from collections import Counter,defaultdict
ROOT=pathlib.Path(r'D:\tmp2b\fm24-db'); sys.path.append(r'D:\tmp2b\fm24\tools\python')
import zstandard as z
codec=runpy.run_path(r'D:\tmp2b\fm24\scripts\modding_read_dbdat.py')
DB=pathlib.Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
P={}
for side in ('client','server'):
    db=(DB/f'{side}_db.dat').read_bytes(); lay=codec['_archive_layout'](db); base=lay['data_base']
    es={(x['path'].split('/')[-1]):x for x in lay['entries']}
    e=es['table_9.dat']; P[side]=z.ZstdDecompressor().decompressobj().decompress(db[base+e['offset']:base+e['offset']+e['packed_size']])
def cands(b,i,lo=13):
    out=[]; needle=struct.pack('<I',i); p=b.find(needle,lo)
    while p>=0:
        if p+13<=len(b):
            c,d=struct.unpack_from('<II',b,p+4)
            if c==d and b[p+12]==0: out.append((p,c))
        p=b.find(needle,p+1)
    return out
b=P['server']; n=struct.unpack_from('<I',b,8)[0]; stop=len(b)-8
C={i:cands(b,i) for i in range(n)}
# forward reachable positions per row (ignoring id monotonic)
fwd=[{13}]
for i in range(n):
    s=set()
    for pos in fwd[-1]:
        for p,rid in C[i]:
            if p>=pos and p+13<=stop: s.add(p+13)
    fwd.append(s)
# backward
bwd=[None]*(n+1); bwd[n]={stop}
for i in range(n-1,-1,-1):
    s=set()
    for pos in bwd[i+1]:
        for p,rid in C[i]:
            if p+13<=pos and p>=13: s.add(p)
    bwd[i]=s
print('server forward widths',[len(x) for x in fwd[:6]],'...',[len(fwd[i]) for i in range(120,130)])
print('server backward widths',[len(x) for x in bwd[:6]])
# contested: rows where >1 candidate in some complete walk
cont=[]
for i in range(n):
    ok=[]
    for p,rid in C[i]:
        e=p+13
        if e in fwd[i+1] and p in bwd[i] and any(p>=q for q in fwd[i]) and True:
            ok.append((p,rid))
    cont.append(len(ok))
print('rows with >1 candidate in a complete walk:',[(i,cont[i]) for i in range(n) if cont[i]>1][:20],'total',sum(1 for x in cont if x>1))
for i in range(n):
    if cont[i]>1:
        p,rid=C[i][0]
        print('row',i,'candidates',[(q,r) for q,r in C[i]][:6])
