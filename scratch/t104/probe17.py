import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
H=14; T=13; ident=d['ident']; lens=d['lens']
def body(i):
    s=H if i==0 else ident[i-1][0]+T
    return raw[s:ident[i][0]]
sel=[x[2] for x in ident]
for i in range(0,60):
    print(i,'sel',sel[i],'len',lens[i], body(i)[:20].hex())
print('...')
print('uid values rows 0..5', [ident[i][1] for i in range(6)])
print('uid row 50,56,60', ident[50][1], ident[56][1], ident[60][1])
