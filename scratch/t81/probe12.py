import runpy, struct
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]

def chains(raw, W=13):
    """All complete ordinal chains starting anywhere. Returns list of pos lists."""
    L=len(raw); n=u32(raw,8)
    cand={}
    for p in range(L-12):
        a,b=u32(raw,p+4),u32(raw,p+8)
        if a==b and a!=0: cand.setdefault(u32(raw,p),[]).append(p)
    # forward DP from any start
    cur={}   # end -> list of (prev, p) but we only need reachability + count
    reach=[set() for _ in range(n)]
    for p in cand.get(0,()):
        reach[0].add(p)
    for j in range(1,n):
        for p in cand.get(j,()):
            lo=p+W-4096
            if any(lo<=s<=p for s in reach[j-1]): reach[j].add(p)
        if not reach[j]: return None, j
    return reach, None

for a,t in [('client',10),('server',10),('client',8),('client',27),('client',47),('server',24),('client',6),('server',6),('client',23),('client',35)]:
    raw=m['load_payload'](a,t); L=len(raw); n=u32(raw,8)
    reach,why=chains(raw)
    if reach is None: print(a,t,'LOST at',why); continue
    ends={p+13 for p in reach[-1]}
    print(a,t,'n',n,'first_reach',len(reach[0]),sorted(reach[0])[:4],'last_reach',len(reach[-1]),
          'end==L-8?',(L-8) in ends,'ends',sorted(ends)[:4])
