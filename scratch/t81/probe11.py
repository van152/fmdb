import runpy, struct
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]

def walk(raw, w=12, H=13):
    L=len(raw); n=u32(raw,8); cand={}
    for p in range(L-w):
        a,b=u32(raw,p+4),u32(raw,p+8)
        if a==b and a!=0: cand.setdefault(u32(raw,p),[]).append(p)
    cur={H}; pos=[]
    for j in range(n):
        reach=set()
        for p in cand.get(j,()):
            if p+w>L: continue
            lo=p+w-4096
            if any(lo<=s<=p for s in cur): reach.add(p)
        if not reach: return None
        if len(reach)>1: return ('amb',j)
        pos.append(next(iter(reach))); cur={p+w for p in reach}
    return pos

targets={}
for a,t in [('client',10),('client',8),('client',27),('client',47),('client',23),('client',24),('server',24),('client',6)]:
    raw=m['load_payload'](a,t); n=u32(raw,8)
    p=walk(raw,13,14)
    if isinstance(p,list):
        uids=[u32(raw,x+4) for x in p]
    else:
        p2=walk(raw,12,13)
        uids=[u32(raw,x+4) for x in p2] if isinstance(p2,list) else []
    targets[(a,t)]={'n':n,'uids':uids}
    print(a,t,'n',n,'uids',len(uids),'distinct',len(set(uids)),'min',min(uids),'max',max(uids))

rc=m['load_payload']('client',2); H,S,n=14,43,56293
for f,off,ref in [('Cnti',10,10),('Cwea',14,27),('Clgi',21,8),('Clri',25,47)]:
    vals=[u32(rc,H+j*S+off) for j in range(n)]
    nn=[v for v in vals if v!=0xFFFFFFFF]
    tgt=targets[('client',ref)]
    ud=set(tgt['uids'])
    uidhit=sum(1 for v in nn if v in ud)
    print(f'{f}@{off} -> t{ref} N={tgt["n"]}: ordinal max={max(nn)} (max/N={max(nn)/tgt["n"]:.4f}, in-domain={sum(1 for v in nn if v<tgt["n"])/len(nn):.4f}) | UID hit={uidhit}/{len(nn)}')
    # reverse coverage
    cov=len({v for v in nn if v<tgt['n']})
    print(f'      reverse coverage {cov}/{tgt["n"]} = {cov/tgt["n"]:.4f}, distinct={len(set(nn))}')
