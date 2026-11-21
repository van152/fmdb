import sys,struct
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
codec=C.codec(); p=C.DB/'lang_update_db.dat'
db=p.read_bytes(); ents=codec['list_tables'](p,'lang_update_db.dat')
base=int(codec['_archive_layout'](db)['data_base'])
z=codec['_zstd_module'](); MAGIC=bytes.fromhex('28b52ffd')
def stream(s,e):
    d=z.ZstdDecompressor(); pos=s; outs=[]
    while pos+4<=e and db[pos:pos+4]==MAGIC:
        o_=d.decompressobj(); o=o_.decompress(db[pos:e])
        if not o: break
        outs.append(o); used=(e-pos)-len(o_.unused_data)
        if not o_.eof or used<=0: break
        pos+=used
    return b''.join(outs)
for nm in ('10_2','10_3','10_0'):
    e=next(x for x in ents if x['path'].endswith(f'/{nm}.dat'))
    out=stream(base+e['offset'],base+e['offset']+e['packed_size'])
    print('==',nm,len(out),'u32@8',struct.unpack_from('<I',out,8)[0] if len(out)>12 else None)
    print('  ',repr(out[12:120]))
