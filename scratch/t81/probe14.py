import runpy, struct
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
def uids_chain(a,t,W=13,H=14):
    raw=m['load_payload'](a,t); L=len(raw); n=u32(raw,8); cand={}
    for p in range(L-12):
        x,y=u32(raw,p+4),u32(raw,p+8)
        if x==y and x!=0: cand.setdefault(u32(raw,p),[]).append(p)
    reach=[set() for _ in range(n)]
    for p in cand.get(0,()): reach[0].add(p)
    for j in range(1,n):
        for p in cand.get(j,()):
            lo=p+W-8192
            if any(lo<=s<=p for s in reach[j-1]): reach[j].add(p)
        if not reach[j]: return None,n,raw
    return [u32(raw,p+4) for p in sorted(reach[-1])],n,raw
rc=m['load_payload']('client',2); H,S,n=14,43,56293
for f,off,ref in [('Cnti',10,10),('Cwea',14,27),('Clgi',21,8),('Clri',25,47)]:
    vals=[u32(rc,H+j*S+off) for j in range(n)]
    nn=[v for v in vals if v!=0xFFFFFFFF]
    u,N,_=uids_chain('client',ref)
    Nt = N
    ud=set(u) if u else set()
    inord=sum(1 for v in nn if v<Nt)
    print(f'{f}@{off} -> t{ref} N={Nt} null={len(vals)-len(nn)}')
    print(f'   ordinal: in-domain {inord}/{len(nn)}={inord/len(nn):.6f} max={max(nn)} max/N={max(nn)/Nt:.4f} distinct={len(set(nn))} reverse_cov={len({v for v in nn if v<Nt})}/{Nt}={len({v for v in nn if v<Nt})/Nt:.4f}')
    print(f'   UID    : hit {sum(1 for v in nn if v in ud)}/{len(nn)}')
