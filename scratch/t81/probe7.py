import runpy, struct, time
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
def chain(raw, n, sel=False):
    pos=0; found=[]
    for j in range(n):
        p=pos; hit=None
        while p+12<=len(raw):
            if u32(raw,p)==j:
                a,b=u32(raw,p+4),u32(raw,p+8)
                if a==b!=0: hit=p; break
            p+=1
        if hit is None: return found,j
        found.append(hit); pos=hit+(13 if sel else 12)
    return found,None
for t in (1,3,25,5,19,41,21,2,10,8,27,47,24,0,7,18,56,6,23,35):
    for a in ('client','server'):
        t0=time.time()
        try:
            raw=m['load_payload'](a,t)
        except Exception as e:
            print(f'{a} {t} LOAD_ERR {type(e).__name__}: {str(e)[:80]}'); continue
        n=u32(raw,8)
        sel = (t==24)
        f,why=chain(raw,n,sel)
        tail=len(raw)-(f[-1]+13) if f else None
        print(f'{a:6s} {t:3d} L={len(raw):9d} n={n:6d} found={len(f):6d} lost={why} tail={tail} {time.time()-t0:.1f}s')
