import runpy, sys, struct
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
def rows_fixed(raw, n, stride, h=13):
    return [raw[h+i*stride:h+(i+1)*stride] for i in range(n)]

for name,(arch,tid,n,stride) in {'city_c':('client',2,56293,43),'cont_c':('client',5,7,34),
    'cont_s':('server',5,7,48),'regi_c':('client',19,28,45),'regi_s':('server',19,28,46)}.items():
    raw=dump['load_payload'](codec,arch,tid)
    print('=====',name,'len',len(raw),'hdr',raw[:13].hex(),'foot',raw[13+n*stride:].hex(), 'close',13+n*stride+9==len(raw))
    rs=rows_fixed(raw,n,stride)
    # per-offset byte listing for first rows
    for i in (0,1,2):
        print(' row',i,' '.join(f'{x:02x}' for x in rs[i]))
    # column distinct counts
    cols=[]
    for o in range(stride):
        vs=[r[o] for r in rs]
        cols.append((o,len(set(vs))))
    print(' byte-distinct:', cols)
