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
n=struct.unpack_from('<I',o,8)[0]; print('declared n',n,'buflen',len(o))
pos=12; i=0
while i<n:
    st=pos
    try:
        key=struct.unpack_from('<I',o,pos)[0]; pos+=4; f=[]
        for _ in range(4):
            L=struct.unpack_from('<I',o,pos)[0]; pos+=4
            if L>500: raise ValueError(f'L={L}')
            f.append(o[pos:pos+L].decode('utf-8','replace')); pos+=L+1
    except Exception as ex:
        print(f'FAIL at rec {i} pos {st}: {ex}'); print('  bytes',o[st:st+48].hex(' ')); break
    i+=1
print('parsed',i,'end pos',pos)
