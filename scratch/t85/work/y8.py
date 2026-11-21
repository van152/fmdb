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
def get(k):
    e=by[k]; return stream(base+e['offset'],base+e['offset']+e['packed_size'])
def parse(out,nstr=4):
    n=struct.unpack_from('<I',out,8)[0]; pos=12; r=[]
    for _ in range(n):
        rid=struct.unpack_from('<I',out,pos)[0]; pos+=4; f=[]
        for _ in range(nstr):
            L=struct.unpack_from('<I',out,pos)[0]; pos+=4
            f.append(out[pos:pos+L].decode('utf-8','replace')); pos+=L+1
        r.append((rid,f))
    return r,pos,len(out)
for k in ('16_9.dat','1000002_9.dat','8_9.dat'):
    r,pos,tot=parse(get(k))
    ids=[x[0] for x in r]
    print(f'== {k} recs={len(r)} consumed={pos}/{tot} ids {min(ids)}..{max(ids)} uniq={len(set(ids))}')
    for rid,f in r[:3]: print('    ',rid,f)
