import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
ident=d['ident']; lens=d['lens']; n=len(ident); sel=[x[2] for x in ident]
starts=[14]+[ident[i][0]+13 for i in range(n-1)]
def body(i): return raw[starts[i]:starts[i]+lens[i]]
def strz(b,e):
    """[u32 l][bytes][0x00] ending at e"""
    if e-5<0 or b[e-1]!=0: return None
    for l in range(0,min(300,e-5)+1):
        p=e-1-l
        if p-4<0: continue
        if struct.unpack_from('<I',b,p-4)[0]!=l: continue
        s=b[p:p+l]
        if 0 in s: continue
        try: s.decode('utf-8')
        except: continue
        return (p-4,l,s.decode())
    return None
dist=collections.Counter(); ok=0; tot=0
for i in range(n):
    b=body(i); g2=strz(b,len(b))
    if not g2: dist['no2']+=1; continue
    g1=strz(b,g2[0])
    if not g1: dist['no1']+=1; continue
    be=g1[0]; tot+=1
    found=False
    for pre in (0,49):
        if be<pre+53: continue
        c=struct.unpack_from('<H',b,pre+33)[0]
        if pre+53+4*c>be: continue
        dist[(pre, be-(pre+53+4*c))]+=1
        found=True
    if not found: dist['nofit']+=1
print('rows with 2 names',tot)
for k,v in sorted(dist.items(), key=lambda kv:-kv[1])[:12]: print(k,v)
