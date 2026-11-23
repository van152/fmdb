import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
H=14; T=13; ident=d['ident']; lens=d['lens']; n=len(ident)
def body(i):
    s=H if i==0 else ident[i-1][0]+T
    return raw[s:ident[i][0]]
sel=[x[2] for x in ident]
def parse_names(b, start):
    p=start; out=[]
    for _ in range(2):
        if p+4>len(b): return None
        l=struct.unpack_from('<I',b,p)[0]
        if l>200 or p+4+l>len(b): return None
        try: s=b[p+4:p+4+l].decode('utf-8')
        except: return None
        out.append(s); p+=4+l
    return (out,p-start) if p==len(b) else None
delta=collections.Counter(); samples=collections.defaultdict(list)
for i in range(n):
    b=body(i); pref=49 if sel[i]==11 else 0
    if len(b)<pref+35: delta['short']+=1; continue
    c=struct.unpack_from('<H',b,pref+33)[0]
    base=pref+53+4*c
    r=parse_names(b,base) if base<=len(b) else None
    if r is None:
        delta[('no',sel[i])]+=1
        if len(samples[('no',sel[i])])<3: samples[('no',sel[i])].append((i,len(b),c,b.hex()))
    else:
        delta[(sel[i], r[1])]+=1
        if r[1]!=8 and len(samples[(sel[i],r[1])])<3: samples[(sel[i],r[1])].append((i,len(b),c,r[0]))
for k,v in sorted(delta.items(), key=lambda kv:-kv[1])[:10]: print(k,v)
for k,v in samples.items(): print(k,v[:2])
