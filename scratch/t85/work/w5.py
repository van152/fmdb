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
by={e['path'].split('/')[-1]:e for e in ents}
fams=collections.defaultdict(list)
for k,e in by.items():
    m=re.match(r'(\d+)_(\d+)\.dat$',k)
    if m: fams[(int(m.group(1)),int(m.group(2)))].append(e['size'])
print('distinct (lang,table) pairs:',len(fams))
tabs=collections.Counter(t for (_,t) in fams)
print('table ids present:',sorted(tabs))
langs=collections.Counter(l for (l,_) in fams)
print('n langs:',len(langs),'sample',sorted(langs)[:12])
print()
for t in sorted(tabs):
    ks=[(l,by[f'{l}_{t}.dat']['size']) for (l,tt) in fams if tt==t]
    print(f'  table {t:2d}: {len(ks)} langs; 1000002 ->',by.get(f'1000002_{t}.dat',{}).get('size'))
