import runpy, struct
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
raw=m['load_payload']('server',10); L=len(raw); n=u32(raw,8)
print('L',L,'n',n,'hdr',raw[:16].hex())
# find all p with ordinal==0 and uid pair
hits=[p for p in range(L-12) if u32(raw,p)==0 and u32(raw,p+4)==u32(raw,p+8)!=0]
print('ordinal0 candidates', hits[:10], len(hits))
hits1=[p for p in range(L-12) if u32(raw,p)==1 and u32(raw,p+4)==u32(raw,p+8)!=0]
print('ordinal1 candidates', hits1[:10], len(hits1))
print('first bytes', raw[14:14+40].hex())
# try greedy from each ordinal0
def greedy(start):
    pos=start; got=[]
    for j in range(n):
        p=pos; hit=None
        while p+12<=L:
            if u32(raw,p)==j and u32(raw,p+4)==u32(raw,p+8)!=0: hit=p; break
            p+=1
        if hit is None: return got, j
        got.append(hit); pos=hit+12
    return got,None
for s in hits[:5]:
    g,why=greedy(s)
    print('start',s,'got',len(g),'lost',why,'tail',L-(g[-1]+12) if g else None)
