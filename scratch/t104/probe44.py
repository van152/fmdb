import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
ident=d['ident']; lens=d['lens']; n=len(ident)
sel=[x[2] for x in ident]
def body(i):
    s=14 if i==0 else ident[i-1][0]+13
    return raw[s:ident[i][0]]
for i in (0,1,2,20,50,89,1162):
    b=body(i)
    print('==',i,'sel',sel[i],'len',len(b))
    print(b.hex())
