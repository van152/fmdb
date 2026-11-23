import runpy, struct, json, io
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
fr=json.load(io.open('scratch/t74/out/frames.json',encoding='utf-8'))['tables']
def solve(raw, lo, hi, W=13, H=14, F=8, maxlen=4096):
    L=len(raw); n=u32(raw,8); c={}
    for p in range(L-12):
        a,b=u32(raw,p+4),u32(raw,p+8)
        if a==b and a!=0: c.setdefault(u32(raw,p),[]).append(p)
    reach=[set() for _ in range(n)]
    for p in c.get(n-1,()):
        if p+W==L-F: reach[n-1].add(p)
    for j in range(n-2,-1,-1):
        for p in c.get(j,()):
            if any(p+W<=s<=p+W+maxlen for s in reach[j+1]): reach[j].add(p)
        if not reach[j]: return None,j
    prev={H}
    for j in range(n):
        keep={p for p in reach[j] if any(lo<=p+W-s<=hi for s in prev)}
        if not keep: return None,j
        reach[j]=keep; prev={p+W for p in keep}
    return reach,None
for t in ('8','27','24','7'):
    for a,v in fr[t]['archives'].items():
        if v.get('count') is None: continue
        raw=m['load_payload'](a,int(t)); lo,hi=v['row_len_range']
        r,why=solve(raw,lo,hi)
        multi=[(j,sorted(s)) for j,s in enumerate(r) if len(s)>1]
        print(t,a,'multi rows',len(multi), multi[:3])
        # uid invariance
        for j,s in multi[:3]:
            print('   row',j,'uids',[u32(raw,p+4) for p in s])
