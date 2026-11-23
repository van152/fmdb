import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
ident=d['ident']; lens=d['lens']; n=len(ident); sel=[x[2] for x in ident]
starts=[14]+[ident[i][0]+13 for i in range(n-1)]
def body(i): return raw[starts[i]:starts[i]+lens[i]]
BASE=33; TAIL=18
def parse(b,pre):
    p=pre; f={}
    if p+33>len(b): return None
    c=struct.unpack_from('<H',b,p+33)[0]
    if p+35+4*c>len(b): return None
    vec=list(struct.unpack_from('<%dI'%c,b,p+35)) if c else []
    p=p+35+4*c
    if p+18+10>len(b): return None
    tail=b[p:p+18]; blk=b[p+18:p+28]; p+=28
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
    return c,vec,tail.hex(),blk.hex(),names
mis=[]
for i in range(n):
    b=body(i); a=parse(b,0); c=parse(b,49)
    if a and not c: v=0
    elif c and not a: v=49
    elif a and c: v='ambig'
    else: v=None
    if v is None: mis.append((i,'FAIL'))
    elif v=='ambig': mis.append((i,'ambig'))
    elif (sel[i]==11) != (v==49): mis.append((i,sel[i],v,len(b)))
print('anomalies',len(mis))
print(mis[:12])
print('anomaly idx range', min(x[0] for x in mis) if mis else None, max(x[0] for x in mis) if mis else None)
