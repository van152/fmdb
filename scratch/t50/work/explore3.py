import os,pathlib,runpy,struct,sys
ROOT=pathlib.Path(r'D:\tmp2b\fm24-db'); sys.path.append(r'D:\tmp2b\fm24\tools\python')
import zstandard as z
codec=runpy.run_path(r'D:\tmp2b\fm24\scripts\modding_read_dbdat.py')
DB=pathlib.Path(os.environ.get('FM24_DB_DIR') or ROOT/'scratch/data')
P={}
for side in ('client','server'):
    db=(DB/f'{side}_db.dat').read_bytes(); lay=codec['_archive_layout'](db); base=lay['data_base']
    es={(x['path'].split('/')[-1]):x for x in lay['entries']}
    for name in ('table_9.dat','table_extra_9.dat'):
        e=es[name]; lo=base+e['offset']
        P[side,name]=z.ZstdDecompressor().decompressobj().decompress(db[lo:lo+e['packed_size']])
for side,name in [('client','table_9.dat'),('server','table_9.dat')]:
    b=P[side,name]
    print('='*60); print(side,name,len(b))
    print('  last 32 bytes hex:',b[-32:].hex())
    print('  idx of ident250:',[p for p in range(len(b)-40,len(b)-12) if struct.unpack_from('<III',b,p)==(250,struct.unpack_from('<I',b,p+4)[0],)*3 and False] )
    # find it directly
    for p in range(13,len(b)-12):
        a,c,d=struct.unpack_from('<III',b,p)
        if a==250 and c==d and b[p+12]==0:
            print('   ident250@',p,'id',c,'tail13 end',p+13,'left',len(b)-(p+13),'left hex',b[p+13:].hex())
    print('  first 40 after header13:',b[13:53].hex())
