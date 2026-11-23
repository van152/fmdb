import runpy, struct, time, collections
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
raw = m['load_payload']('server',24); n=u32(raw,8); L=len(raw)
t0=time.time(); pos=0; found=[]; why=None
for j in range(n):
    p=pos; hit=None
    while p+12<=L:
        if u32(raw,p)==j:
            a,b=u32(raw,p+4),u32(raw,p+8)
            if a==b!=0: hit=p; break
        p+=1
    if hit is None: why='lost at %d'%j; break
    found.append(hit); pos=hit+13
print('found',len(found),why,'%.1fs'%(time.time()-t0))
print('tail',L-pos, raw[pos:].hex())
gaps=[found[i+1]-found[i] for i in range(len(found)-1)]
print('gap min/max',min(gaps),max(gaps))
sel=collections.Counter(raw[f+12] for f in found)
print('selector',dict(sel))
uids=[u32(raw,f+4) for f in found]
print('uid distinct',len(set(uids)),'min',min(uids),'max',max(uids))
