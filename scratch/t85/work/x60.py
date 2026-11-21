import sys
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
codec=C.codec(); p=C.DB/'lang_update_db.dat'
db=p.read_bytes(); ents=codec['list_tables'](p,'lang_update_db.dat')
base=int(codec['_archive_layout'](db)['data_base'])
z=codec['_zstd_module']()
hits=[]
for e in ents:
    s=base+int(e['offset']); end=s+int(e['packed_size'])
    try: out=z.ZstdDecompressor().decompress(db[s:end])
    except Exception: continue
    for n in (b'England',b'Singapore',b'Algeria'):
        if n in out: hits.append((e['path'],n.decode(),len(out)))
for h in hits: print(h)
print('total',len(hits))
