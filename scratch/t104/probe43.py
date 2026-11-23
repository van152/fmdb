import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
ident=d['ident']; lens=d['lens']; n=len(ident)
sel=[x[2] for x in ident]
def body(i):
    s=ident[i][0]; return raw[s:s+lens[i]]
for i in (0,1,50,1162,655):
    b=body(i); print(i,'sel',sel[i],'len',len(b)); print(b.hex()[:200]); print('tail',b[-40:].hex())
