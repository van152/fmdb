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
for side in ('client','server'):
    b=P[side]; n=struct.unpack_from('<I',b,8)[0]
    starts=[12]; pos=12
    for i in range(1,n):
        for d in range(0,30000):
            q=pos+d
            if q>=len(b): break
            if ok(b,q,i) is not None: starts.append(q); pos=q; break
    ends=starts[1:]+[len(b)]
    print('='*70); print(side,'len',len(b),'records',len(starts))
    print('  trailer last-16 share of records:',Counter(b[ends[k]-16:ends[k]].hex()[-10:] for k in range(len(starts))).most_common(4))
    # positional byte profile at row_end - j
    for j in range(1,10):
        c=Counter(b[e-j] for e in ends[:-1])
        print(f'  end-{j} byte hist',dict(c.most_common(4)),'n distinct',len(c))
    print('  count of b"fffafafaff" occurrences',b.count(bytes.fromhex('fffafafaff')))
    print('  count of b"0001fffafafaff" occurrences',b.count(bytes.fromhex('0001fffafafaff')))
    # u32 at end-8..end-4 for each record
    print('  u32@end-8 sample',[hex(struct.unpack_from('<I',b,e-8)[0]) for e in ends[:6]])
    print('  u32@end-4 sample',[struct.unpack_from('<I',b,e-4)[0] for e in ends[:-1]][:10])
    print('  last 20 record ends u32@-4',[struct.unpack_from('<I',b,e-4)[0] for e in ends[-21:-1]])
