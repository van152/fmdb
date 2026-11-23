import runpy, struct, collections
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
for a,t,S,p in [('client',6,16,3),('server',6,40,27),('client',23,14,1),('server',23,14,1),('client',35,15,2),('server',35,15,2)]:
    raw = m['load_payload'](a,t); L=len(raw); n=u32(raw,8)
    print('='*70); print(a,t,'L',L,'n',n,'H',14,'S',S,'p',p,'tail',L-14-n*S)
    ok = all(u32(raw,14+j*S+p)==j and u32(raw,14+j*S+p+4)==u32(raw,14+j*S+p+8)!=0 for j in range(n))
    mk = collections.Counter(raw[14+j*S+S-1] for j in range(n))
    print(' identity',ok,'marker',dict(mk))
    for off in range(S-13):
        col = [raw[14+j*S+off] for j in range(n)]
        c = collections.Counter(col)
        print(f'  off{off:2d} u8 distinct={len(c)} top={c.most_common(5)}')
