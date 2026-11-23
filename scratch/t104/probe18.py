import sys, struct, runpy, collections, json, re
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
hits=[]
for i in range(len(ident)):
    b=body(i)
    if re.search(rb'[A-Za-z]{4,}', b): hits.append(i)
print('rows with ascii words', len(hits), hits[:8])
for i in hits[:4]:
    print('row',i,'sel',sel[i],'len',lens[i])
    print('  ', body(i).hex())
