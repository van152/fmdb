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
    n=struct.unpack_from('<I',o,8)[0]; pos=12; r=[]
    for _ in range(n):
        key=struct.unpack_from('<I',o,pos)[0]; pos+=4; f=[]
        for _ in range(4):
            L=struct.unpack_from('<I',o,pos)[0]; pos+=4
            f.append(o[pos:pos+L].decode('utf-8','replace')); pos+=L+1
        r.append((key,f))
    return r,pos,len(o)
o=get('16_9.dat'); r,pos,tot=parse(o)
print('recs',len(r),'consumed',pos,'/',tot,'keys',r[0][0],'..',r[-1][0])
d={k:v for k,v in r}
for row,exp in ((0,'ALG'),(1,'ANG'),(55,'CHN'),(139,'ENG'),(145,'GER'),(189,'BRA'),(250,'?')):
    for off in (0,5):
        v=d.get(row+off)
        print(f'  t10row {row:3d} + {off} -> key {row+off:3d} : {v[2] if v else None} (want {exp})')
