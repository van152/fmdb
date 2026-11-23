import runpy, struct
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]

def chain(raw, W=13, H=14, maxlen=4096):
    """greedy ordinal chain; returns (positions, end, ok)"""
    L=len(raw); n=u32(raw,8); pos=H; got=[]
    for j in range(n):
        p=pos; hit=None
        while p+W<=L:
            if u32(raw,p)==j and u32(raw,p+4)==u32(raw,p+8)!=0: hit=p; break
            p+=1
        if hit is None: return got,None,('lost',j)
        got.append(hit); pos=hit+W
    return got,pos,None

# team (24) server only
rt=m['load_payload']('server',24); pos,end,why=chain(rt)
print('t24 rows',len(pos),'end',end,'L-8',len(rt)-8,'why',why)
team_uids=[u32(rt,p+4) for p in pos]
team_ord=set(range(len(pos)))
print('team uids distinct',len(set(team_uids)))
print('selector', {v: sum(1 for p in pos if rt[p+12]==v) for v in sorted({rt[p+12] for p in pos})})

# derby Dtm1@4 Dtm2@8 : ordinal vs uid vs club
rd=m['load_payload']('client',18); H,S,n=14,69,1567
# derby rows are variable! S=69..195. need per-row starts -> use identity chain
dpos,dend,dwhy=chain(rd)
print('t18 rows',len(dpos),'why',dwhy)
# row start: identity ends at p+13, row = [4 names][num][identity]; need names parse
def derby_rows(raw):
    n=u32(raw,8); p=14; rows=[]
    for j in range(n):
        s=p; nb=0
        for _ in range(4):
            ln=u32(raw,p); nb+=ln; p+=4+ln
        # numeric region then 13B identity
        # find identity: search forward for ord==j uid pair
        q=p
        while q<len(raw):
            if u32(raw,q)==j and u32(raw,q+4)==u32(raw,q+8)!=0: break
            q+=1
        rows.append((s,p,q))
        p=q+13
    return rows
drows=derby_rows(rd)
print('derby rows',len(drows))
# numeric region length per archive
nl=[q-num for (s,num,q) in drows]
print('num len distinct',sorted(set(nl)))
