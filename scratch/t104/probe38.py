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
def nstart(b):
    for l2 in range(0,min(260,len(b))+1):
        p2=len(b)-l2
        if p2-4<0: continue
        if struct.unpack_from('<I',b,p2-4)[0]!=l2: continue
        s=b[p2:p2+l2]
        if s and s[-1]==0: s=s[:-1]
        if 0 in s: continue
        try: s.decode('utf-8')
        except: continue
        for l1 in range(0,min(260,p2-4)+1):
            p1=p2-4-l1
            if p1-4<0: continue
            if struct.unpack_from('<I',b,p1-4)[0]!=l1: continue
            s1=b[p1:p1+l1]
            if s1 and s1[-1]==0: s1=s1[:-1]
            if 0 in s1: continue
            try: s1.decode('utf-8')
            except: continue
            return p1-4
    return None
rem=collections.Counter(); ex=[]
for i in range(n):
    b=body(i)
    if nstart(b) is not None: continue
    c=struct.unpack_from('<H',b,33)[0]
    r=len(b)-53-2-4*c
    rem[(sel[i],r)]+=1
    if len(ex)<10: ex.append((i,sel[i],len(b),c,b[53:].hex()))
print(rem.most_common(20))
for e in ex: print(e)
