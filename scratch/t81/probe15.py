import runpy, struct
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]

def cand(raw):
    L=len(raw); out={}
    for p in range(L-12):
        a,b=u32(raw,p+4),u32(raw,p+8)
        if a==b and a!=0: out.setdefault(u32(raw,p),[]).append(p)
    return out

def backward(raw, W=13, maxlen=4096):
    L=len(raw); n=u32(raw,8); c=cand(raw)
    reach=[set() for _ in range(n)]
    for p in c.get(n-1,()):
        if p+W==L-8: reach[n-1].add(p)
    for j in range(n-2,-1,-1):
        for p in c.get(j,()):
            if any(p+W <= s <= p+W+maxlen for s in reach[j+1]): reach[j].add(p)
        if not reach[j]: return reach,j
    return reach,None

for a,t in [('client',10),('client',8),('client',27),('client',47),('server',24),('client',6),('server',6),('client',23),('client',35),('client',2),('client',3),('client',25),('client',18),('client',7),('client',21),('client',0),('client',56),('client',5),('client',19),('client',41)]:
    raw=m['load_payload'](a,t)
    r,why=backward(raw)
    if why is not None: print(a,t,'LOST',why); continue
    sizes=[len(s) for s in r]
    print(f'{a:6s} {t:3d} n={len(r):6d} all_singleton={max(sizes)==1} max_reach={max(sizes)} n_multi={sum(1 for s in sizes if s>1)}')
