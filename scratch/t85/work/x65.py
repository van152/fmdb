import sys,struct
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
e=next(x for x in ents if x['path'].endswith('/10_9.dat'))
out=stream(db,base+e['offset'],base+e['offset']+e['packed_size'])
print('len',len(out))
print(out[:8].hex(' '))
print('u32@8',struct.unpack_from('<I',out,8)[0])
p2=12
for k in range(6):
    ln=struct.unpack_from('<I',out,p2)[0]
    print(f'  [{k}] at {p2} len={ln} {out[p2+4:p2+4+ln]!r}')
    p2+=4+ln
