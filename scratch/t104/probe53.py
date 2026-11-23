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
NT=[('n184',4),('n188',4),('n220',4),('n224',1),('n192',4),('n204',4),('n208',4),('n212',4),('n216',4),('n196',4),('n200',4),('n225',1),('n226',1),('n228',1),('n229',1),('n230',1),('n231',1),('n227',1)]
def parse(b,nat,minname=1):
    f={}
    if nat:
        if len(b)<49: return None
        p=0
        for k,w in NT:
            f[k]=int.from_bytes(b[p:p+w],'little'); p+=w
        f['ncount']=b[48]; p=49
    else: p=0
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
    if p+10>len(b): return None
    blk=b[p:p+10]; p+=10
    names=[]
    for _ in range(2):
        if p+5>len(b): return None
        l=struct.unpack_from('<I',b,p)[0]
        if l<minname or p+4+l+1>len(b) or b[p+4+l]!=0: return None
        s=b[p+4:p+4+l]
        if 0 in s: return None
        try: names.append(s.decode('utf-8'))
        except: return None
        p+=4+l+1
    if p!=len(b): return None
    return dict(f=f,c=c,vec=vec,blk=blk.hex(),names=names)
stat=collections.Counter(); rows={}
for i in range(n):
    b=body(i); a=parse(b,False); c=parse(b,True)
    if a and c: stat[(sel[i],'ambig')]+=1
    elif a: stat[(sel[i],'base')]+=1
    elif c: stat[(sel[i],'nat')]+=1
    else: stat[(sel[i],'FAIL')]+=1
print(stat)
