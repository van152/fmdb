import runpy, struct
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
def back(raw, F, W=13, maxlen=8192):
    L=len(raw); n=u32(raw,8); c={}
    for p in range(L-12):
        a,b=u32(raw,p+4),u32(raw,p+8)
        if a==b and a!=0: c.setdefault(u32(raw,p),[]).append(p)
    reach=[set() for _ in range(n)]
    for p in c.get(n-1,()):
        if p+W==L-F: reach[n-1].add(p)
    if not reach[n-1]: return None,0
    for j in range(n-2,-1,-1):
        for p in c.get(j,()):
            if any(p+W<=s<=p+W+maxlen for s in reach[j+1]): reach[j].add(p)
        if not reach[j]: return None,j
    return reach,None
for a,t in [('client',10),('server',10)]:
    raw=m['load_payload'](a,t); L=len(raw); n=u32(raw,8)
    for F in (8,9,10):
        r,why=back(raw,F)
        if r is None: print(a,t,'F',F,'LOST',why); continue
        sz=[len(s) for s in r]
        print(a,t,'F',F,'n',n,'singleton',max(sz)==1,'maxreach',max(sz),'first',sorted(r[0])[:3],'L',L)
