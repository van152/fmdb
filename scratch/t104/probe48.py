import sys, struct, runpy, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
ident=d['ident']; lens=d['lens']; n=len(ident); sel=[x[2] for x in ident]
starts=[14]+[ident[i][0]+13 for i in range(n-1)]
def body(i):
    return raw[starts[i]:starts[i]+lens[i]]
for i in (0,50,89,1162):
    b=body(i)
    print('===',i,'sel',sel[i],'len',len(b))
    for off in range(0,len(b),8):
        print('  %3d'%off, b[off:off+8].hex())
