import sys,struct
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
codec=C.codec(); p=C.DB/'lang_update_db.dat'
db=p.read_bytes(); ents=codec['list_tables'](p,'lang_update_db.dat')
base=int(codec['_archive_layout'](db)['data_base'])
z=codec['_zstd_module'](); MG=bytes.fromhex('28b52ffd')
def stream(s,e):
    d=z.ZstdDecompressor(); pos=s; outs=[]
    while pos+4<=e and db[pos:pos+4]==MG:
        o_=d.decompressobj(); o=o_.decompress(db[pos:e])
        if not o: break
        outs.append(o); used=(e-pos)-len(o_.unused_data)
        if not o_.eof or used<=0: break
        pos+=used
    return b''.join(outs)
by={e['path'].split('/')[-1]:e for e in ents}
e=by['16_9.dat']; o=stream(base+e['offset'],base+e['offset']+e['packed_size'])
pos=12
for step in range(14):
    key=struct.unpack_from('<I',o,pos)[0]; print(f'pos={pos:5d} key={key}')
    pos+=4
    for si in range(4):
        L=struct.unpack_from('<I',o,pos)[0]
        raw=o[pos+4:pos+4+L]
        print(f'    s{si} L={L:5d} {raw[:40]!r}')
        pos+=4+L
        if L<2000 and o[pos:pos+1]==b'\x00': pos+=1; print('      +NUL')
