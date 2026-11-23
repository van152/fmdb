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
def strz(b,e):
    """parse [u32 l][bytes][0x00] ending at e"""
    if e-5<0: return None
    if b[e-1]!=0: return None
    for l in range(0,min(200,e-5)+1):
        p=e-1-l
        if p-4<0: continue
        if struct.unpack_from('<I',b,p-4)[0]!=l: continue
        try: s=b[p:p+l].decode('utf-8')
        except: continue
        if 0 in b[p:p+l]: continue
        return (p-4,l,s)
    return None
def tail2z(b):
    g2=strz(b,len(b))
    if not g2: return None
    g1=strz(b,g2[0])
    if not g1: return None
    return g1,g2
res=collections.Counter(); bl=collections.Counter(); extra=collections.Counter()
for i in range(n):
    b=body(i)
    t=tail2z(b)
    if not t: res[('no2z',sel[i])]+=1; continue
    be=t[0][0]
    found=None
    for c in range(0,200):
        st=be-(12+53+4*c)
        if st<0: break
        if struct.unpack_from('<H',b,st+33)[0]==c: found=(c,st); break
    if found is None: res[('noc',sel[i])]+=1; continue
    res[(sel[i],'ok2z')]+=1
    bl[sel[i]]+=1
print(res); print('n2z rows by sel',bl)
