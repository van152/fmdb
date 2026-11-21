import sys,struct,re
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
names={e['path'].split('/')[-1]:e for e in ents}
print('any *_10.dat:',[k for k in names if k.endswith('_10.dat')])
for k in ('8_10.dat','7_10.dat','32_10.dat'):
    print(k,'present' if k in names else 'ABSENT')
# what tables map to nation? table_10 -> none. Check *_10 vs *_9 counts
import collections
fams=collections.defaultdict(list)
for k in names:
    m=re.match(r'(\d+)_(\d+)\.dat$',k)
    if m: fams[m.group(1)].append(int(m.group(2)))
for lang in sorted(fams,key=lambda x:int(x))[:6]:
    print('lang',lang,'tables',sorted(fams[lang]))
