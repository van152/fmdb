import runpy, struct, time, bisect
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]

def cand_index(raw):
    """single pass: value u32(p) -> list of p with uid pair equal & nonzero"""
    L=len(raw); out={}
    for p in range(0, L-12):
        a=u32(raw,p+4); b=u32(raw,p+8)
        if a==b and a!=0:
            out.setdefault(u32(raw,p),[]).append(p)
    return out

def frame_dp(raw, maxlen=1024, H=14):
    L=len(raw); n=u32(raw,8); cand=cand_index(raw)
    # counts: pos -> count
    cur={H:1}
    starts=[H]; paths=[{H:1}]
    for j in range(n):
        nxt={}
        for p in cand.get(j,()):
            end=p+13
            if end>L: continue
            lo=end-maxlen
            # any s in cur with lo<=s<=p
            for s,c in cur.items():
                if lo<=s<=p:
                    nxt[end]=nxt.get(end,0)+c
        if not nxt: return {"ok":False,"lost_at":j,"rows":j}
        cur=nxt; paths.append(cur)
    final=L-8
    return {"ok":True,"rows":n,"solutions":cur.get(final,0),"end":final,
            "pos_states":sum(len(x) for x in paths),
            "ambiguity":{k:v for k,v in paths[-1].items()}}

for a,t in [('client',6),('server',6),('client',23),('client',35),('client',10),('client',2),('client',8),('client',27),('client',47),('server',24),('client',3),('client',25),('client',18),('client',7),('client',21),('client',0),('client',56),('client',5),('client',19),('client',41)]:
    t0=time.time(); raw=m['load_payload'](a,t)
    r=frame_dp(raw)
    print(f'{a:6s} {t:3d} L={len(raw):9d} ok={r["ok"]} sol={r.get("solutions")} states={r.get("pos_states")} {time.time()-t0:.1f}s')
