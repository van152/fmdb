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
n=struct.unpack_from('<I',o,8)[0]
pos=12; recs=[]; bad=None
for i in range(n):
    st=pos
    key=struct.unpack_from('<I',o,pos)[0]; pos+=4; f=[]
    for si in range(4):
        L=struct.unpack_from('<I',o,pos)[0]; pos+=4
        if L>300 or pos+L>len(o):
            bad=(i,st,si,pos,L); break
        f.append(o[pos:pos+L].decode('utf-8','replace')); pos+=L+1
    if bad: break
    recs.append((key,f))
print('parsed',len(recs),'of',n,'pos',pos,'len',len(o),'bad',bad)
if bad:
    i,st,si,p2,L=bad
    print('  context:',o[st:st+60].hex(' '))
else:
    print('  first',recs[0],'last',recs[-1])
