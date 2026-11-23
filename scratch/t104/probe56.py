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
def variant(b):
    nm=names(b)
    if not nm: return None
    be=nm[0][0]
    for pre in (0,49):
        if be < pre+BASE+2+TAIL+10: continue
        c=struct.unpack_from('<H',b,pre+BASE)[0]
        if pre+BASE+2+4*c+TAIL+10==be: return pre,c
    return None
mis=[]; corr=collections.Counter()
for i in range(n):
    b=body(i); v=variant(b)
    if not v: corr[(sel[i],'novariant')]+=1; continue
    corr[(sel[i],v[0])]+=1
    if (sel[i]==10)!= (v[0]==0): mis.append((i,sel[i],v,len(b),b[:49].hex()))
print(corr)
print('mismatch',len(mis))
for x in mis[:6]: print(x)
print('prefix4 of nat rows sample')
for i in range(0,60,6):
    print(i, body(i)[:12].hex())
