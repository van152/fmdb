import sys,collections
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
codec=C.codec(); p=C.DB/'lang_update_db.dat'
db=p.read_bytes(); ents=codec['list_tables'](p,'lang_update_db.dat')
base=int(codec['_archive_layout'](db)['data_base'])
z=codec['_zstd_module'](); MAGIC=bytes.fromhex('28b52ffd')
def stream(d_,s,e):
    d=z.ZstdDecompressor(); pos=s; outs=[]
    while pos+4<=e and d_[pos:pos+4]==MAGIC:
        obj=d.decompressobj(); o=obj.decompress(d_[pos:e])
        if not o: break
        outs.append(o); used=(e-pos)-len(obj.unused_data)
        if not obj.eof or used<=0: break
        pos+=used
    return b''.join(outs)
hits=[]
for e in ents:
    s=base+int(e['offset']); end=s+int(e['packed_size'])
    out=stream(db,s,end)
    for n in (b'England',b'Singapore',b'Algeria'):
        if n in out: hits.append((e['path'],n.decode(),len(out),out.count(n)))
for h in sorted(hits): print(h)
print('total',len(hits))
