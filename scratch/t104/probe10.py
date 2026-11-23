import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
H=14; T=13; ident=d['ident']; n=len(ident); lens=d['lens']
def body(i):
    s=H if i==0 else ident[i-1][0]+T
    return raw[s:ident[i][0]]
sel=[x[2] for x in ident]
def names_at(b, off):
    # try u32 len + utf8 twice
    try:
        l1=struct.unpack_from('<I',b,off)[0]
        if l1>64 or off+4+l1>len(b): return None
        s1=b[off+4:off+4+l1]
        try: s1.decode('utf-8')
        except: return None
        p=off+4+l1
        l2=struct.unpack_from('<I',b,p)[0]
        if l2>64 or p+4+l2>len(b): return None
        s2=b[p+4:p+4+l2]
        try: s2.decode('utf-8')
        except: return None
        if p+4+l2 != len(b): return None
        return (l1,s1.decode('utf-8'),l2,s2.decode('utf-8'))
    except Exception: return None
# find rows where names parse from end with TEAM layout
res=collections.Counter(); samples=[]
for i in range(n):
    b=body(i)
    pref = 49 if sel[i]==11 else 0
    if len(b)<pref+53: 
        res[('short',sel[i])]+=1; continue
    c=struct.unpack_from('<H',b,pref+33)[0]
    if len(b)<pref+53+4*c: res[('c_toolarge',sel[i])]+=1; continue
    rest=b[pref+53+4*c:]
    nm=names_at(b, len(b)- (0))
    # base size = len(rest) - (4+l1+4+l2) if names present
    if rest:
        # try to detect names by scanning: last part
        found=None
        for base in range(0, 40):
            off=pref+53+4*c+base
            if off>len(b): break
            nm=names_at(b, off)
            if nm: found=(base,nm); break
        if found: res[('name',sel[i],found[0])]+=1
        else: res[('noname_tail',sel[i],len(rest))]+=1
    else:
        res[('exact',sel[i])]+=1
for k,v in sorted(res.items(), key=lambda kv:-kv[1])[:25]:
    print(k,v)
