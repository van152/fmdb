import runpy, struct
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
def rows13(raw, H=14, W=13):
    L=len(raw); n=u32(raw,8); c={}
    for p in range(L-12):
        a,b=u32(raw,p+4),u32(raw,p+8)
        if a==b and a!=0: c.setdefault(u32(raw,p),[]).append(p)
    reach=[set() for _ in range(n)]
    for p in c.get(n-1,()):
        if p+W==L-8: reach[n-1].add(p)
    for j in range(n-2,-1,-1):
        for p in c.get(j,()):
            if any(p+W<=s<=p+W+8192 for s in reach[j+1]): reach[j].add(p)
    return [min(s) for s in reach]
# local_region t47: row = 41+5k, identity at end-13
lr=m['load_payload']('client',47); pos=rows13(lr)
print('lr rows',len(pos))
lnat=[u32(lr,p-13+4-4-0) for p in pos]  # placeholder
# real offsets: identity ord@-13 uid@-9; body starts p-13-len... need row start
# recompute row starts: row start = identity_abs - (rowlen-13). rowlen = 41+5k, k at ? use (len-41)%5
starts=[]
for p in pos:
    s=p-13
    # find row start by scanning back for len in 41+5k
    found=None
    for k in range(0,40):
        L=41+5*k
        if s-L+13>=0 and s-L+13 >= (starts[-1] if starts else 14):
            found=s-L; break
    starts.append(found)
print('starts',starts[:6], 'diff', [starts[i+1]-starts[i] for i in range(5)])
# t76c says: Lpop@4 u32, u8@0, u32@24, 12xu8@8, items 5B
for i in range(3):
    st=starts[i]; ln=pos[i]-13-st
    print(i,'start',st,'len',ln+13,'biz',lr[st:pos[i]-13].hex())
