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
def parse_team(b,p0):
    p=p0+33
    if p+2>len(b): return None
    c=struct.unpack_from('<H',b,p)[0]; p+=2
    if p+4*c>len(b): return None
    vecs=list(struct.unpack_from('<%dI'%c,b,p)) if c else []
    p+=4*c
    names=[]
    for _ in range(2):
        if p+4>len(b): return None
        l=struct.unpack_from('<I',b,p)[0]
        if l>400 or p+4+l+1>len(b): return None
        s=b[p+4:p+4+l]
        if b[p+4+l]!=0: return None
        if 0 in s: return None
        try: names.append(s.decode('utf-8'))
        except: return None
        p+=4+l+1
    if p+12!=len(b): return None
    return c,vecs,names,b[p:p+12],p0
def parse_nat(b):
    if len(b)<49: return None
    cn=b[48]
    p=49
    r=parse_team(b,p)
    return (cn,r) if r else None
res=collections.Counter(); samples=[]
for i in range(n):
    b=body(i)
    if sel[i]==11:
        r=parse_nat(b)
        if r: res[('nat',True)]+=1
        else:
            r=parse_team(b,0)
            res[('nat_as_team',bool(r))]+=1
            if len(samples)<5: samples.append((i,sel[i],len(b),b.hex()[:120]))
    else:
        r=parse_team(b,0)
        res[('team',bool(r))]+=1
        if not r and len(samples)<5: samples.append((i,sel[i],len(b),b.hex()[:120]))
print(res)
for s in samples: print(s)
