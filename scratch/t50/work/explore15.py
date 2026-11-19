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
def starts(b,i):
    out=[]; needle=struct.pack('<I',i); p=b.find(needle,12)
    while p>=0:
        if p+8<=len(b):
            ln=struct.unpack_from('<I',b,p+4)[0]
            if 1<=ln<=120 and p+8+ln<=len(b):
                nm=b[p+8:p+8+ln]
                if all(0x20<=x<0x7f or x>=0x80 for x in nm): out.append((p,ln,nm.hex()))
        p=b.find(needle,p+1)
    return out
for side in ('client','server'):
    b=P[side]; print('='*70); print(side,'len',len(b))
    for i in [0,1,2,55,56,57,250]:
        print('  ord',i,starts(b,i)[:6],'n=',len(starts(b,i)))
    hist=Counter(len(starts(b,i)) for i in range(251))
    print('  candidate histogram',dict(sorted(hist.items())))
