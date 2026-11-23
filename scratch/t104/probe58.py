import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
ident=d['ident']; lens=d['lens']; n=len(ident); sel=[x[2] for x in ident]
starts=[14]+[ident[i][0]+13 for i in range(n-1)]
def body(i): return raw[starts[i]:starts[i]+lens[i]]
BASE=[('f176',1),('f171',1),('f168',2),('f80',4),('f96',4),('f88',4),('f120',4),('f128',4),('f152',4),('f175',1),('f104',4)]
TAIL=[('f136',4),('f144',4),('f170',1),('f172',1),('f173',1),('f174',1),('f177',1),('f112',4),('f178',1)]
def parse(b,pre,blk=10):
    p=pre; f={}
    for k,w in BASE:
        if p+w>len(b): return None
        f[k]=int.from_bytes(b[p:p+w],'little'); p+=w
    if p+2>len(b): return None
    c=struct.unpack_from('<H',b,p)[0]; p+=2
    if p+4*c>len(b): return None
    vec=list(struct.unpack_from('<%dI'%c,b,p)) if c else []; p+=4*c
    for k,w in TAIL:
        if p+w>len(b): return None
        f[k]=int.from_bytes(b[p:p+w],'little'); p+=w
    if p+blk>len(b): return None
    blk_b=b[p:p+blk]; p+=blk
    names=[]
    for _ in range(2):
        if p+4>len(b): return None
        l=struct.unpack_from('<I',b,p)[0]
        if p+4+l>len(b): return None
        s=b[p+4:p+4+l]
        if 0 in s: return None
        try: names.append(s.decode('utf-8'))
        except: return None
        p+=4+l
    if p!=len(b): return None
    return dict(f=f,c=c,vec=vec,blk=blk_b.hex(),names=names)
stat=collections.Counter(); fails=[]
for i in range(n):
    b=body(i)
    a=parse(b,0); c=parse(b,49)
    if a and c: stat[(sel[i],'ambig')]+=1
    elif a: stat[(sel[i],'base')]+=1
    elif c: stat[(sel[i],'nat49')]+=1
    else:
        stat[(sel[i],'FAIL')]+=1
        if len(fails)<6: fails.append((i,sel[i],len(b),b[:60].hex()))
print(stat)
for x in fails: print(x)
# constant prefix census
pre33=collections.Counter()
for i in range(n):
    b=body(i); pre33[(b[:33], sel[i])]+=1
print('distinct 33B prefixes', len(pre33))
for k,v in pre33.most_common(4): print(v, k[1], k[0].hex())
for i in (0,50,134,351):
    print('row',i,'sel',sel[i],'len',len(body(i)), body(i)[:49].hex())
