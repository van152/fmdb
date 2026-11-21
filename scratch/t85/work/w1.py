import sys,struct,json
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
def get(k):
    e=by[k]; return stream(base+e['offset'],base+e['offset']+e['packed_size'])
def parse(o):
    n=struct.unpack_from('<I',o,8)[0]; pos=12; r={}
    for _ in range(n):
        key=struct.unpack_from('<I',o,pos)[0]; pos+=4; f=[]
        for si in range(4):
            L=struct.unpack_from('<I',o,pos)[0]; pos+=4
            f.append(o[pos:pos+L].decode('utf-8','replace')); pos+=L
            if si!=2: pos+=1
        r[key]=f
    return r
L=parse(get('16_9.dat'))
for duni,row,label in ((765,139,'England'),(110,55,'China PR'),(771,145,'Germany'),
                       (1651,189,'Brazil'),(1649,187,'Argentina'),(116,61,'Japan'),
                       (390,120,'USA'),(1435,177,'Australia'),(62003815,248,'Yugoslavia')):
    print(f'{label:12s} row={row:3d} duni={duni:9d} -> {L.get(duni)}')
