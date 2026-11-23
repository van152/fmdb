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
def parse(out,n):
    pos=12; r=[]
    for _ in range(n):
        key=struct.unpack_from('<I',out,pos)[0]; pos+=4; f=[]
        for _ in range(4):
            L=struct.unpack_from('<I',out,pos)[0]; pos+=4
            f.append(out[pos:pos+L].decode('utf-8','replace')); pos+=L+1
        r.append((key,f))
        if pos<len(out) and out[pos]==0 and pos+4<=len(out):
            # optional declension block: [u8 n][n x ([u32][str\0][u16][u8])]
            save=pos; nd=out[pos]; pos+=1; ok=True
            try:
                for _ in range(nd):
                    L=struct.unpack_from('<I',out,pos)[0]; pos+=4+L+1+3
            except Exception: ok=False
            if not ok: pos=save
    return r,pos,len(out)
for k in ('16_9.dat','1000002_9.dat'):
    n=struct.unpack_from('<I',get(k),8)[0]
    r,pos,tot=parse(get(k),n)
    print(f'== {k} n={n} parsed={len(r)} end={pos}/{tot}')
    codes=[x[1][2] for x in r]
    print('   codes[:12]',codes[:12])
    d={x[0]:x[1] for x in r}
    print('   key->name for keys 0..8:',[(kk,d.get(kk,[None])[0]) for kk in range(0,9)])
    for probe in ('ENG','CHN','BRA','GER','ALG'):
        hit=[x for x in r if x[1][2]==probe]
        print('   code',probe,'->',hit[0] if hit else None)
