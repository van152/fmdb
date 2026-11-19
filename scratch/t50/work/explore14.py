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
def recname(b,p):
    if p+8>len(b): return None
    idx,ln=struct.unpack_from('<II',b,p)
    if ln>120 or p+8+ln>len(b): return None
    nm=b[p+8:p+8+ln]
    if any(x<0x20 for x in nm): return None
    return idx,ln,nm
for side in ('client','server'):
    b=P[side]; n=struct.unpack_from('<I',b,8)[0]
    print('='*60); print(side,'len',len(b),'count',n)
    pos=12; rows=[]
    for i in range(n):
        picked=None
        for d in range(0,20000):
            r=recname(b,pos+d)
            if r and r[0]==i: picked=(pos+d,r); break
        if not picked: print(' stop at ordinal',i,'pos',pos); break
        rows.append((i,picked[0],picked[1][1],picked[1][2].decode('utf-8','replace'))); 
        pos=picked[0]+8+picked[1][1]
    print(' walked',len(rows),'pos after',pos,'payload',len(b),'left',len(b)-pos)
    for r in rows[:5]: print('  ',r)
    print('  last',rows[-1] if rows else None)
    print('  left hex',b[pos:pos+64].hex())
