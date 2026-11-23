import runpy, struct, time
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]

def cands(raw, w):
    L=len(raw); out={}
    for p in range(0, L-w):
        a=u32(raw,p+4); b=u32(raw,p+8)
        if a==b and a!=0:
            out.setdefault(u32(raw,p),[]).append(p)
    return out

def solve(raw, w=13, H=14, maxlen=2048, nrows=None):
    L=len(raw); n=nrows or u32(raw,8)
    cand=cands(raw,w)
    cur={H}; amb=0; per=[]
    for j in range(n):
        reach=set()
        for p in cand.get(j,()):
            if p+w>L: continue
            lo=p+w-maxlen
            if any(lo<=s<=p for s in cur): reach.add(p)
        per.append(len(reach))
        if not reach: return {"ok":False,"lost":j,"rows":j}
        if len(reach)>1: amb+=1
        cur={p+w for p in reach}
    end=L-8
    return {"ok":True,"rows":n,"final_reach":len([p for p in cur if p==end]) if end in cur else 0,
            "ambiguous_rows":amb,"multi_reach":sum(1 for x in per if x>1)}

for a,t in [('client',10),('server',10),('client',6),('server',6),('client',23),('client',35),('client',2),('client',8),('client',27),('client',47),('server',24),('client',3),('client',25),('client',18),('client',7),('client',21),('client',0),('client',56),('client',5),('client',19),('client',41)]:
    raw=m['load_payload'](a,t)
    for w in (13,12):
        t0=time.time(); r=solve(raw,w)
        print(f'{a:6s} {t:3d} w={w} ok={r["ok"]} final={r.get("final_reach")} amb={r.get("ambiguous_rows")} multi={r.get("multi_reach")} {time.time()-t0:.1f}s')
