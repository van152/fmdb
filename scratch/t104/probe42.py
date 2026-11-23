import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
H=14; T=13; ident=d["ident"]; n=len(ident); sel=[x[2] for x in ident]
def body(i):
    s=H if i==0 else ident[i-1][0]
    return raw[s:ident[i][0]-T]
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
        if b[p+4+l]!=0 or 0 in s: return None
        try: names.append(s.decode('utf-8'))
        except: return None
        p+=4+l+1
    return c,vecs,names,b[p:p0+33] if p<=len(b) else None,p,len(b)
res=collections.Counter(); ok=[]
for i in range(n):
    b=body(i)
    r=parse_team(b,0)
    if r: res[('team',sel[i])]+=1; ok.append((i,r))
    else: res[('fail',sel[i])]+=1
print(res)
print(ok[:3])
for i in (0,1,1162,50):
    b=body(i); print(i,sel[i],len(b),'pre33',b[:33].hex())
