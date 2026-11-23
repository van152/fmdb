import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
ident=d['ident']; lens=d['lens']; n=len(ident); sel=[x[2] for x in ident]
starts=[14]+[ident[i][0]+13 for i in range(n-1)]
def body(i): return raw[starts[i]:starts[i]+lens[i]]
def parse(b,pre):
    p=pre
    if p+35>len(b): return None
    c=struct.unpack_from('<H',b,p+33)[0]
    if p+35+4*c>len(b): return None
    vec=list(struct.unpack_from('<%dI'%c,b,p+35)) if c else []
    p=p+35+4*c
    if p+28>len(b): return None
    tail=b[p:p+18].hex(); blk=b[p+18:p+28].hex(); p+=28
    names=[]
    for _ in range(2):
        if p+5>len(b): return None
        l=struct.unpack_from('<I',b,p)[0]
        if p+4+l+1>len(b) or b[p+4+l]!=0: return None
        s=b[p+4:p+4+l]
        if 0 in s: return None
        try: names.append(s.decode('utf-8'))
        except: return None
        p+=4+l+1
    if p!=len(b): return None
    return dict(pre=pre,c=c,vec=vec,tail=tail,blk=blk,names=names)
for i in (0,1,50,89,93,655,1162,3041,488):
    b=body(i)
    r=parse(b,0) or parse(b,49)
    print(i,'sel',sel[i],'len',len(b),json.dumps(r) if r else 'FAIL')
    if r: print('   base33@%d'%r['pre'], b[r['pre']:r['pre']+33].hex())
