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
    """returns (base_end, l1,l2) if b ends with two u32-len-prefixed utf8 strings"""
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
res=collections.Counter(); bases=collections.Counter(); natstarts=collections.Counter()
samples=[]
for i in range(n):
    b=body(i); tn=tail_names(b)
    if tn is None: res[('noname',sel[i])]+=1; continue
    be,l1,l2=tn
    # try each c
    found=None
    for c in range(0, 200):
        start=be-(12+53+4*c)
        if start<0: break
        if struct.unpack_from('<H',b,start+33)[0]==c:
            found=(c,start); break
    if found is None: res[('noc',sel[i])]+=1; continue
    c,start=found
    blen=be-(start+53+4*c)
    res[(sel[i],'ok')]+=1
    bases[(sel[i],blen)]+=1
    if sel[i]==11: natstarts[(start-49, c)]+=1
for k,v in sorted(res.items(), key=lambda kv:-kv[1]): print(k,v)
print('base len dist', bases.most_common(10))
print('nat start-49 & c', sorted(natstarts.items(), key=lambda kv:-kv[1])[:15])
