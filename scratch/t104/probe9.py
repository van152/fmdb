import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
H=14; T=13; ident=d['ident']; n=len(ident)
def body(i):
    s=H if i==0 else ident[i-1][0]+T
    return raw[s:ident[i][0]]
sel=[x[2] for x in ident]; lens=d['lens']
rows73=[i for i in range(n) if sel[i]==10 and lens[i]==73]
print('rows of len 73 (TEAM,c=0,no strings):',len(rows73))
# column profile
import array
cols=collections.defaultdict(collections.Counter)
for i in rows73:
    b=body(i)
    for o in range(73):
        cols[o][b[o]]+=1
prof=[]
for o in range(73):
    c=cols[o]
    prof.append((o,len(c),sorted(c.items(), key=lambda kv:-kv[1])[:4]))
for o,k,v in prof:
    print(o,k,v)
