import sys,struct,pathlib
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
codec=C.codec()
p=C.DB/'lang_update_db.dat'
ents=codec['list_tables'](p,'lang_update_db.dat')
db=p.read_bytes()
lay=codec['_archive_layout'](db)
base=int(lay['data_base'])
print('base',base,'entries',len(ents))
z=codec['_zstd_module']()
for e in ents:
    if e['path'].endswith('_10.dat'):
        s=base+e['offset']; end=s+e['packed_size']
        out=z.ZstdDecompressor().decompress(db[s:end])
        print(e['path'],'payload',len(out),'declared',e['size'])
        print('  head',out[:32].hex(' '))
        print('  ascii',repr(out[:120]))
