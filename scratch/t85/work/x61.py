import sys
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
codec=C.codec(); p=C.DB/'lang_update_db.dat'
db=p.read_bytes(); ents=codec['list_tables'](p,'lang_update_db.dat')
base=int(codec['_archive_layout'](db)['data_base'])
z=codec['_zstd_module']()
bad=0; ok=0
for e in ents[:6]:
    s=base+int(e['offset']); end=s+int(e['packed_size'])
    print(e['path'],'member',s,end,'declared',e['size'])
    print('  bytes',db[s:s+12].hex(' '))
    try:
        out=z.ZstdDecompressor().decompress(db[s:end]); print('  decomp',len(out)); ok+=1
    except Exception as ex: print('  ERR',ex); bad+=1
print('ok',ok,'bad',bad)
