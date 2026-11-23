import sys, struct, runpy, collections, json
sys.path.insert(0,'D:/tmp2b/fm24/tools/python'); sys.path.insert(0,'scripts')
d=json.load(open('scratch/t104/path.json'))
m=runpy.run_path('scripts/t38_multiframe.py', run_name='p')
codec=m['_codec'](); cache={}
raw=m['load_payload_mf'](codec,'server',24,cache)
ident=d['ident']; n=len(ident); sel=[x[2] for x in ident]
def body(i):
    s=14 if i==0 else ident[i-1][0]+13
    return raw[s:ident[i][0]]
def nstart(b):
    for l2 in range(0,min(260,len(b))+1):
        p2=len(b)-l2
        if p2-4<0: continue
        if struct.unpack_from('<I',b,p2-4)[0]!=l2: continue
        s=b[p2:p2+l2]
        if s and s[-1]==0: s=s[:-1]
        if not s or 0 in s: continue
        try: s.decode('utf-8')
        except: continue
        for l1 in range(0,min(260,p2-4)+1):
            p1=p2-4-l1
            if p1-4<0: continue
            if struct.unpack_from('<I',b,p1-4)[0]!=l1: continue
            s1=b[p1:p1+l1]
            if s1 and s1[-1]==0: s1=s1[:-1]
            if not s1 or 0 in s1: continue
            try: s1.decode('utf-8')
            except: continue
            return p1-4
    return None
gap=collections.Counter(); cpos=collections.Counter()
for i in range(n):
    b=body(i); ns=nstart(b)
    if ns is None: continue
    c=struct.unpack_from('<H',b,33)[0]
    gap[(ns-(35+4*c))]+=1
    if ns-(35+4*c)==30:
        g=b[35+4*c:ns]
        cpos[(g[:2].hex(), g[2:4].hex(), g[4:6].hex(), g[6:].hex()[:8])]+=0
print('gap dist', gap.most_common(8))
# for gap==30 rows, look at the 30 bytes structure vs c
samp=[]
for i in range(n):
    b=body(i); ns=nstart(b)
    if ns is None: continue
    c=struct.unpack_from('<H',b,33)[0]
    if ns-(35+4*c)!=30: continue
    g=b[35+4*c:ns]
    samp.append((i,sel[i],c,g.hex(),b[:33].hex()))
    if len(samp)>=6: break
for s in samp: print(s)
