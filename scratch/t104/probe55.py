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
def names(b):
    g2=strz(b,len(b))
    if not g2: return None
    g1=strz(b,g2[0])
    if not g1: return None
    return g1,g2
bad=[]
for i in range(n):
    if sel[i]==10: continue
    b=body(i); nm=names(b)
    be=nm[0][0]
    pre=be-(53+4*struct.unpack_from('<H',b,49+33)[0])-10-49 if len(b)>82 else -1
    # compute count from nat layout
    c=struct.unpack_from('<H',b,49+33)[0]
    exp=49+33+2+4*c+28
    if exp!=be: bad.append((i,sel[i],len(b),c,be,exp))
print('nat rows bad', len(bad), 'of', sum(1 for s in sel if s!=10))
for x in bad[:8]: print(x)
