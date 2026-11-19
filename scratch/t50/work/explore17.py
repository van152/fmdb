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
def ok(b,p,i,maxln=200):
    if p+8>len(b): return None
    a,ln=struct.unpack_from('<II',b,p)
    if a!=i or ln>maxln or p+8+ln>len(b): return None
    nm=b[p+8:p+8+ln]
    if any(x<0x20 for x in nm): return None
    return ln
for side in ('client','server'):
    b=P[side]; n=struct.unpack_from('<I',b,8)[0]
    print('='*70); print(side,'len',len(b))
    starts=[12]
    pos=12
    for i in range(1,n):
        f=None
        for d in range(0,30000):
            q=pos+d
            if q>=len(b): break
            ln=ok(b,q,i)
            if ln is not None: f=q; break
        if f is None: print(' fail at',i); break
        starts.append(f); pos=f
    print(' starts',len(starts))
    lens=[(starts[k+1]-starts[k]) if k+1<len(starts) else None for k in range(len(starts))]
    print(' first rec lens',lens[:6])
    print(' last start',starts[-1],'rec len to end',len(b)-starts[-1])
    print(' tail hex',b[starts[-1]:][-160:].hex())
