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
sel=[x[2] for x in ident]
def tail_names(b):
    for l2 in range(0, min(200,len(b))+1):
        p2=len(b)-l2
        if p2-4<0: continue
        if struct.unpack_from('<I',b,p2-4)[0]!=l2: continue
        try: b[p2:p2+l2].decode('utf-8')
        except: continue
        e1=p2-4
        for l1 in range(0, min(200,e1)+1):
            p1=e1-l1
            if p1-4<0: continue
            if struct.unpack_from('<I',b,p1-4)[0]!=l1: continue
            try: b[p1:p1+l1].decode('utf-8')
            except: continue
            return (p1-4, l1, l2)
    return None
bad=[i for i in range(n) if tail_names(body(i)) is None]
print('bad count', len(bad), 'sel dist', collections.Counter(sel[i] for i in bad))
print('len dist', collections.Counter(len(body(i)) for i in bad).most_common(12))
for i in bad[:6]:
    b=body(i); print('---',i,'sel',sel[i],'len',len(b)); print(b.hex())
