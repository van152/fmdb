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
raw=m['load_payload']('server',10)
g,why=fwd(raw,13,13)
gaps=[g[i+1]-g[i] for i in range(len(g)-1)]
print('rows',len(g),'gap min/max/mean',min(gaps),max(gaps),sum(gaps)/len(gaps))
print('rows near 171:', [(i,g[i]) for i in range(168,175)])
print('last rows', g[-3:], 'L', len(raw))
