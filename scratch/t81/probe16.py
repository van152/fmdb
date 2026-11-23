import runpy, struct
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
def back(raw, W=13, maxlen=4096):
    L=len(raw); n=u32(raw,8); c={}
    for p in range(L-12):
        a,b=u32(raw,p+4),u32(raw,p+8)
        if a==b and a!=0: c.setdefault(u32(raw,p),[]).append(p)
    reach=[set() for _ in range(n)]
    for p in c.get(n-1,()):
        if p+W==L-8: reach[n-1].add(p)
    for j in range(n-2,-1,-1):
        for p in c.get(j,()):
            if any(p+W<=s<=p+W+maxlen for s in reach[j+1]): reach[j].add(p)
        if not reach[j]: return None
    return reach
for a,t in [('client',10),('client',8),('client',27),('server',24),('client',6),('server',6),('client',23),('client',35),('client',2),('client',3),('client',25)]:
    raw=m['load_payload'](a,t); r=back(raw)
    if r is None: print(a,t,'LOST'); continue
    inv = all(len({u32(raw,p+4) for p in s})==1 for s in r if s)
    tot = sum(len({u32(raw,p+4) for p in s}) for s in r if s)
    print(f'{a} {t} uid_set_invariant={inv} total_distinct_across_cands={tot} n={len(r)}')
