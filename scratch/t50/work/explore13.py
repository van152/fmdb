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
for side in ('client','server'):
    b=P[side]; n=struct.unpack_from('<I',b,8)[0]
    print('='*60); print(side,'len',len(b),'count',n)
    # candidates for record start: u32 == expected ordinal at pos, plausible u32 len, sane name
    def starts_ok(p,idx):
        if p+8>len(b): return None
        a,ln=struct.unpack_from('<II',b,p)
        if a!=idx: return None
        if not (1<=ln<=64) or p+8+ln>len(b): return None
        nm=b[p+8:p+8+ln]
        if sum(1 for x in nm if x<0x20) > 0: return None
        return (a,ln,nm)
    pos=12; rows=[]
    for i in range(n):
        best=None
        for d in range(0,4000):
            r=starts_ok(pos+d,i)
            if r: best=(pos+d,r); break
        if not best: rows.append(None); print(' no start for',i,'from',pos); break
        rows.append(best[0]); pos=best[0]
        # advance past the name
        pos=best[0]+8+best[1][1]
    print(' starts found',len(rows),'last',rows[-1] if rows else None,'len',len(b))
    if all(x is not None for x in rows):
        for k in range(min(4,len(rows))):
            s=rows[k]; e_=rows[k+1] if k+1<len(rows) else len(b)
            print(f'  rec{k} [{s},{e_}) len={e_-s} name={b[s+8:s+8+struct.unpack_from("<I",b,s+4)[0]]!r}')
