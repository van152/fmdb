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

def back_names(b):
    """strict backwards: body ends with [u32 l2][s2][u32 l1][s1] ... returns start of s1 block"""
    if len(b)<8: return None
    l2=struct.unpack_from('<I',b,len(b)-4)[0]
    # find s2 end = len(b) ; s2 len l2 ; prefix l2 at len-4-l2
    # actually structure: [u32 l1][s1][u32 l2][s2] with s2 ending at end
    # try both orders by scanning
    return None

def try_tail(b):
    """try to parse [u32 l1][s1][u32 l2][s2] ending exactly at len(b)"""
    out=[]
    for l2 in range(0, min(80,len(b)-4)+1):
        p2=len(b)-l2
        if p2-4<0: continue
        v=struct.unpack_from('<I',b,p2-4)[0]
        if v!=l2: continue
        s2=b[p2:p2+l2]
        try: s2.decode('utf-8')
        except: continue
        # now preceding: [u32 l1][s1] ending at p2-4
        e1=p2-4
        for l1 in range(0, min(80,e1-4)+1):
            p1=e1-l1
            if p1-4<0: continue
            v1=struct.unpack_from('<I',b,p1-4)[0]
            if v1!=l1: continue
            s1=b[p1:p1+l1]
            try: s1.decode('utf-8')
            except: continue
            out.append((p1-4, s1, s2))
    return out

res=collections.Counter(); samples={}
for i in range(n):
    b=body(i); cands=try_tail(b)
    if not cands: res[('notail',sel[i])]+=1; continue
    # prefer unique
    if len(cands)>1: res[('multi',sel[i],len(cands))]+=1
    for st,s1,s2 in cands:
        delta=st-53-4*0-(49 if sel[i]==11 else 0)
        res[(sel[i], 'delta', delta)]+=1
print('--- delta hist (c=0 only counted) ---')
for k,v in sorted(res.items(), key=lambda kv:-kv[1])[:20]: print(k,v)
# now with c
res2=collections.Counter()
for i in range(n):
    b=body(i)
    pref=49 if sel[i]==11 else 0
    if len(b)<pref+35: res2[('short',sel[i])]+=1; continue
    c=struct.unpack_from('<H',b,pref+33)[0]
    cands=try_tail(b)
    if not cands: res2[('notail',sel[i],c==0)]+=1; continue
    for st,s1,s2 in cands:
        delta=st-pref-53-4*c
        res2[(sel[i],delta)]+=1
print('--- delta with c ---')
for k,v in sorted(res2.items(), key=lambda kv:-kv[1])[:20]: print(k,v)
