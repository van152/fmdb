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
def parse(b, nat, basefix=12):
    p=0
    if nat:
        if len(b)<49: return None
        cn=b[48]; p=49
        p+=0   # items unknown len -> handled outside
        return ('nat_item', cn, p)
    return None
stats=collections.Counter(); samples=[]
for i in range(n):
    b=body(i)
    pref=49 if sel[i]==11 else 0
    # try team-only
    ok=None
    for c_off in [0]:
        if len(b)<pref+35: continue
        c=struct.unpack_from('<H',b,pref+33)[0]
        p=pref+53+4*c
        for fix in (12,):
            if p+fix>len(b): continue
            nm=names2(b,p+fix)
            if nm is not None: ok=(c,fix,nm); break
        if ok: break
    if ok: stats[('team',sel[i])]+=1
    else:
        stats[('fail',sel[i])]+=1
        if len(samples)<8: samples.append((i,sel[i],len(b),b.hex()))
print(stats)
for s in samples: print(s[0],s[1],s[2],s[3][:160])
