import sys
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
codec=C.codec(); p=C.DB/'lang_update_db.dat'
db=p.read_bytes(); ents=codec['list_tables'](p,'lang_update_db.dat')
base=int(codec['_archive_layout'](db)['data_base'])
z=codec['_zstd_module']()
MAGIC=bytes.fromhex('28b52ffd')
def stream(archive_db,start,end):
    d=z.ZstdDecompressor(); pos=start; outs=[]
    while pos+4<=end and archive_db[pos:pos+4]==MAGIC:
        obj=d.decompressobj(); o=obj.decompress(archive_db[pos:end])
        if not o: break
        outs.append(o)
        used=(end-pos)-len(obj.unused_data)
        if not obj.eof or used<=0: break
        pos+=used
    return b''.join(outs)
tot=0
for e in ents:
    s=base+int(e['offset']); end=s+int(e['packed_size'])
    out=stream(db,s,end)
    if len(out)!=e['size']:
        print('MISMATCH',e['path'],len(out),e['size']); tot+=1
print('mismatches',tot,'of',len(ents))
