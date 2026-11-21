import runpy, struct
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
def chains(raw, W):
    L=len(raw); n=u32(raw,8); cand={}
    for p in range(L-12):
        a,b=u32(raw,p+4),u32(raw,p+8)
        if a==b and a!=0: cand.setdefault(u32(raw,p),[]).append(p)
    reach=[set() for _ in range(n)]
    for p in cand.get(0,()): reach[0].add(p)
    for j in range(1,n):
        for p in cand.get(j,()):
            lo=p+W-8192
            if any(lo<=s<=p for s in reach[j-1]): reach[j].add(p)
        if not reach[j]: return reach,j
    return reach,None
raw=m['load_payload']('server',10); L=len(raw); n=u32(raw,8)
for W in (12,13,14):
    r,why=chains(raw,W)
    if why: print('W',W,'LOST at',why); continue
    ends={p+13 for p in r[-1]}
    print('W',W,'first',len(r[0]),sorted(r[0])[:3],'last',len(r[-1]),'end',sorted(ends)[:3],'L-8',L-8)
