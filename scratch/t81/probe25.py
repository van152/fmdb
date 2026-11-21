import runpy, struct, json, io
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
fr=json.load(io.open('scratch/t74/out/frames.json',encoding='utf-8'))['tables']

def solve(raw, lo, hi, W=13, H=14, F=8, maxlen=4096):
    L=len(raw); n=u32(raw,8)
    c={}
    for p in range(L-12):
        a,b=u32(raw,p+4),u32(raw,p+8)
        if a==b and a!=0: c.setdefault(u32(raw,p),[]).append(p)
    reach=[set() for _ in range(n)]
    for p in c.get(n-1,()):
        if p+W==L-F: reach[n-1].add(p)
    for j in range(n-2,-1,-1):
        for p in c.get(j,()):
            if any(p+W<=s<=p+W+maxlen for s in reach[j+1]): reach[j].add(p)
        if not reach[j]: return None,('lost',j)
    prev={H}
    for j in range(n):
        keep={p for p in reach[j] if any(lo<=p+W-s<=hi for s in prev)}
        if not keep: return None,('window',j)
        reach[j]=keep; prev={p+W for p in keep}
    return reach,None

for t in ('8','27','47','24','7','18','0','21','56'):
    for a,v in fr[t]['archives'].items():
        if v.get('count') is None: continue
        raw=m['load_payload'](a,int(t))
        lo,hi=v['row_len_range']
        r,why=solve(raw,lo,hi)
        if r is None: print(t,a,'FAIL',why); continue
        sz=[len(s) for s in r]
        print(f'{t:3s} {a:6s} n={len(r):6d} unique={max(sz)==1} maxreach={max(sz)} multi={sum(1 for x in sz if x>1)} range={lo}-{hi}')
