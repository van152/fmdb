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
def strz(b,e):
    if e-5<0: return None
    for l in range(0,min(200,e-5)+1):
        p=e-1-l
        if p-4<0: continue
        if struct.unpack_from('<I',b,p-4)[0]!=l: continue
        s=b[p:p+l]
        if 0 in s: return None if False else None
        try: s.decode('utf-8')
        except: return None
        return (p-4,l)
    return None
# robust names_start: last u32 len whose region decodes utf8 (may include trailing NUL)
def nstart(b):
    best=None
    for l2 in range(0,min(260,len(b))+1):
        p2=len(b)-l2
        if p2-4<0: continue
        if struct.unpack_from('<I',b,p2-4)[0]!=l2: continue
        s=b[p2:p2+l2]
        if s and s[-1]==0: s=s[:-1]
        if 0 in s: continue
        try: s.decode('utf-8')
        except: continue
        # first string
        for l1 in range(0,min(260,p2-4)+1):
            p1=p2-4-l1
            if p1-4<0: continue
            if struct.unpack_from('<I',b,p1-4)[0]!=l1: continue
            s1=b[p1:p1+l1]
            if s1 and s1[-1]==0: s1=s1[:-1]
            if 0 in s1: continue
            try: s1.decode('utf-8')
            except: continue
            return p1-4
    return None
res=collections.Counter(); form=collections.Counter()
for i in range(n):
    b=body(i); ns=nstart(b)
    if ns is None: res[('noname',sel[i])]+=1; continue
    hit=None
    for so in (0,1,2,3,4,49,50,48):
        for c in range(0,400):
            if so+65+4*c==ns and so+35<=len(b) and struct.unpack_from('<H',b,so+33)[0]==c:
                hit=(so,c); break
        if hit: break
    if hit: form[(sel[i],hit[0])]+=1; res[(sel[i],'ok')]+=1
    else: res[('noframe',sel[i])]+=1
print(res); print(form.most_common(12))
