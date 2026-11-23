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
def parse(b):
    res=[]
    for pre in (0,49):
        if pre>=len(b): continue
        p=pre; f={}
        okk=True
        for k,w in BASE:
            if p+w>len(b): okk=False; break
            f[k]=int.from_bytes(b[p:p+w],'little'); p+=w
        if not okk: continue
        if p+2>len(b): continue
        c=struct.unpack_from('<H',b,p)[0]; p+=2
        if p+4*c>len(b): continue
        vec=list(struct.unpack_from('<%dI'%c,b,p)) if c else []; p+=4*c
        for k,w in TAIL:
            if p+w>len(b): okk=False; break
            f[k]=int.from_bytes(b[p:p+w],'little'); p+=w
        if not okk: continue
        if p+10>len(b): continue
        blk=b[p:p+10]; p+=10
        names=[]
        for _ in range(2):
            if p+5>len(b): okk=False; break
            l=struct.unpack_from('<I',b,p)[0]
            if p+4+l+1>len(b) or b[p+4+l]!=0: okk=False; break
            s=b[p+4:p+4+l]
            if 0 in s: okk=False; break
            try: names.append(s.decode('utf-8'))
            except: okk=False; break
            p+=4+l+1
        if not okk or p!=len(b): continue
        res.append(dict(pre=pre,f=f,c=c,vec=vec,blk=blk.hex(),names=names))
    return res
stat=collections.Counter(); both=0; examples=[]
for i in range(n):
    b=body(i); r=parse(b)
    if len(r)==0: stat[('fail',sel[i])]+=1
    elif len(r)==2: stat[('both',sel[i])]+=1; both+=1
    else: stat[(sel[i], r[0]['pre'])]+=1
    if i<3 or i in (50,1162,655,3041): examples.append((i,sel[i],len(b),r))
print(stat, 'both',both)
for e in examples: print(e[0],'sel',e[1],'len',e[2],json.dumps(e[3])[:300])
