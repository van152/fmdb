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
    p=start
    out=[]
    for _ in range(2):
        if p+4>len(b): return None
        l=struct.unpack_from('<I',b,p)[0]
        if l>200 or p+4+l>len(b): return None
        try: s=b[p+4:p+4+l].decode('utf-8')
        except: return None
        out.append(s); p+=4+l
    return (out,p) if p==len(b) else None
ok=0; fail=[]
tails=collections.Counter()
for i in range(n):
    b=body(i); pref=49 if sel[i]==11 else 0
    if pref:
        # nat: prefix 49 + count byte
        if len(b)<pref+1: fail.append((i,'short_prefix')); continue
        cnt=b[pref]
        if cnt!=0: tails[('natcnt',cnt)]+=1
        start=pref+1
    else:
        start=0
    if len(b)<start+35: fail.append((i,'short')); continue
    c=struct.unpack_from('<H',b,start+33)[0]
    base=start+53+4*c
    r=parse_names(b,base)
    if r: ok+=1; tails[('ok',sel[i])]+=1
    else:
        # try search forward for names
        found=None
        for extra in range(1,60):
            rr=parse_names(b,base+extra)
            if rr: found=extra; break
        tails[('shift',sel[i],found)]+=1
        if len(fail)<10: fail.append((i,len(b),c,sel[i],found,b.hex()[:120]))
print('ok',ok,'of',n)
print('fail sample',fail[:5])
for k,v in sorted(tails.items(), key=lambda kv:-kv[1])[:14]: print(k,v)
