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
def hexdump(b,lo,hi):
    for k in range(lo,hi,32):
        chunk=b[k:min(k+32,hi)]
        print(f'{k:6d} {chunk.hex():<64} {"".join(chr(x) if 32<=x<127 else "." for x in chunk)}')
c=P['client']; s=P['server']
print('=== client blocks 0..3 (16..2229) ==='); hexdump(c,16,2229)
