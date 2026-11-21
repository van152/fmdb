import sys,struct,json,collections
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
# all nation dunis: from lang db keys (250 distinct, excludes row0/1)
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
n=struct.unpack_from('<I',o,8)[0]; pos=12; dunis=set()
for _ in range(n):
    k=struct.unpack_from('<I',o,pos)[0]; pos+=4; dunis.add(k)
    for si in range(4):
        L=struct.unpack_from('<I',o,pos)[0]; pos+=4+L+(0 if si==2 else 1)
print('dunis',len(dunis))
rows=[json.loads(l) for l in open('scratch/t50/out/profiles/table_client_extra_9.rows.jsonl',encoding='utf-8')]
items=[]
for r in rows:
    b=bytes.fromhex(r['raw_hex']); nl=r['marker']['name_len']; t=b[8+nl:]
    for k in range(t[6]): items.append(t[8+27*k:8+27*(k+1)])
print('items',len(items))
hits=collections.Counter()
for it in items:
    for off in (1,3,5,7,9):
        v=struct.unpack_from('<H',it,off)[0]
        if v in dunis: hits[off]+=1
print('u16 lanes whose value is a nation duni:',dict(hits),'of',len(items))
