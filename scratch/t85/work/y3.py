import sys,struct,re,collections
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
def recs(out):
    n=struct.unpack_from('<I',out,8)[0]; pos=12; r=[]
    for _ in range(n):
        k=struct.unpack_from('<I',out,pos)[0]; pos+=4; r.append((k,out,pos))
        # need to walk; handled below by caller
    return r
by={e['path'].split('/')[-1]:e for e in ents}
print('%-12s %6s %s'%('member','count','first key0'))
for k,e in sorted(by.items()):
    if not k.endswith('_9.dat'): continue
    out=stream(base+e['offset'],base+e['offset']+e['packed_size'])
    n=struct.unpack_from('<I',out,8)[0]
    keys=[struct.unpack_from('<I',out,12)[0] if n else None]
    print('%-12s %6d %s'%(k,n,keys[0]))
