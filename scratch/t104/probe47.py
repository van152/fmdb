import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
ident=d['ident']; lens=d['lens']; n=len(ident); sel=[x[2] for x in ident]
def body(i):
    s=14 if i==0 else ident[i-1][0]+13
    return raw[s:s+lens[i]]
# wire order from 1411a1280.c
ORD=[('f176',1),('f171',1),('f168',2),('f80',4),('f96',4),('f88',4),('f120',4),('f128',4),
     ('f152',4),('f175',1),('f104',4)]
TAIL=[('f136',4),('f144',4),('f170',1),('f172',1),('f173',1),('f174',1),('f177',1),('f112',4),('f178',1)]
def parse(b, p0=0):
    p=p0; f={}
    for k,w in ORD:
        if p+w>len(b): return None
        f[k]=int.from_bytes(b[p:p+w],'little'); p+=w
    if p+2>len(b): return None
    c=struct.unpack_from('<H',b,p)[0]; p+=2
    if p+4*c>len(b): return None
    vec=list(struct.unpack_from('<%dI'%c,b,p)) if c else []
    p+=4*c
    for k,w in TAIL:
        if p+w>len(b): return None
        f[k]=int.from_bytes(b[p:p+w],'little'); p+=w
    names=[]
    for _ in range(2):
        if p+4>len(b): return None
        l=struct.unpack_from('<I',b,p)[0]
        if l>400 or p+4+l>len(b): return None
        s=b[p+4:p+4+l]
        if 0 in s: return None
        try: names.append(s.decode('utf-8'))
        except: return None
        p+=4+l
    return dict(p=p,f=f,c=c,vec=vec,names=names,rest=b[p:])
res=collections.Counter(); rests=collections.Counter()
for i in range(n):
    b=body(i); r=parse(b)
    if r is None: res[('fail',sel[i])]+=1; continue
    res[('ok',sel[i])]+=1; rests[len(r['rest'])]+=1
print(res); print('rest lens',rests.most_common(8))
for i in (0,1,50,89,1162,655):
    b=body(i); r=parse(b)
    print(i,sel[i],len(b),'names',r['names'],'rest',r['rest'].hex() if r else None)
