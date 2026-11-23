import runpy, struct
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
def fwd(raw, W, H):
    L=len(raw); n=u32(raw,8); pos=H; got=[]
    for j in range(n):
        p=pos; hit=None
        while p+W<=L:
            if u32(raw,p)==j and u32(raw,p+4)==u32(raw,p+8)!=0: hit=p; break
            p+=1
        if hit is None: return got,j
        got.append(hit); pos=hit+W
    return got,None
for a,t in [('client',10),('server',10)]:
    raw=m['load_payload'](a,t); L=len(raw); n=u32(raw,8)
    print('==',a,t,'L',L,'n',n)
    for W in (12,13):
        for H in (13,14):
            g,why=fwd(raw,W,H)
            print('  W',W,'H',H,'found',len(g),'lost',why,'end',(g[-1]+W) if g else None,'L-8',L-8)
