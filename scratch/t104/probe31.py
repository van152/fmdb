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
def names2(b,p):
    out=[]
    for _ in range(2):
        if p+4>len(b): return None
        l=struct.unpack_from('<I',b,p)[0]
        if l>300 or p+4+l>len(b): return None
        try: s=b[p+4:p+4+l].decode('utf-8')
        except: return None
        out.append(s); p+=4+l
    return out if p==len(b) else None
nat=[i for i in range(n) if sel[i]==11]
print('nat rows',len(nat))
for isz in range(5,25):
    ok=0
    for i in nat:
        b=body(i)
        if len(b)<49: continue
        cn=b[48]
        p=49+isz*cn
        if p+35>len(b): continue
        c=struct.unpack_from('<H',b,p+33)[0]
        p2=p+53+4*c
        if names2(b,p2) is not None: ok+=1
    print('itemsize',isz,'ok',ok,'/',len(nat))
