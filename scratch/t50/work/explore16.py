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
def starts(b,i,lo=12,allow0=True):
    out=[]; needle=struct.pack('<I',i); p=b.find(needle,lo)
    while p>=0:
        if p+8<=len(b):
            ln=struct.unpack_from('<I',b,p+4)[0]
            if (1 if not allow0 else 0)<=ln<=120 and p+8+ln<=len(b):
                nm=b[p+8:p+8+ln]
                if all(0x20<=x<0x7f or x>=0x80 for x in nm): out.append((p,ln,len(out)))
        p=b.find(needle,p+1)
    return out
for side in ('client','server'):
    b=P[side]; print('='*70); print(side,'len',len(b))
    miss=[i for i in range(251) if not starts(b,i)]
    print(' missing (allow0):',len(miss),miss[:20])
    # positions of all found starts, check ordering/monotonic
    pos=[]
    for i in range(251):
        c=starts(b,i)
        if c: pos.append((i,c[0][0],c[0][1],len(c)))
    print(' found',len(pos))
    mono=all(pos[k][1]<pos[k+1][1] for k in range(len(pos)-1))
    print(' monotonic:',mono)
    bad=[(pos[k],pos[k+1]) for k in range(len(pos)-1) if pos[k][1]>=pos[k+1][1]]
    print(' non-monotonic pairs',bad[:5])
