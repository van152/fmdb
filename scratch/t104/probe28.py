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
def try_row(b, nat):
    p=0
    cnt_nat=None
    if nat:
        if len(b)<49: return None
        p=48
        cnt_nat=b[48]; p=49
        p+=12*cnt_nat
    if len(b)<p+35: return None
    c=struct.unpack_from('<H',b,p+33)[0]
    p+=53+4*c
    if len(b)<p+12: return None
    p+=12
    for _ in range(2):
        if p+4>len(b): return None
        l=struct.unpack_from('<I',b,p)[0]
        if l>300 or p+4+l>len(b): return None
        try: b[p+4:p+4+l].decode('utf-8')
        except: return None
        p+=4+l
    return p==len(b), cnt_nat, c
stats=collections.Counter(); bad=[]
for i in range(n):
    b=body(i)
    r=try_row(b, sel[i]==11)
    if r is True:
        stats[(sel[i],'ok')]+=1
    else:
        # try the other branch
        alt=try_row(b, sel[i]!=11)
        stats[(sel[i],'fail_alt_'+str(alt))]+=1
        if len(bad)<6: bad.append((i,sel[i],len(b),r,alt,b.hex()[:100]))
print(stats)
for x in bad: print(x)
