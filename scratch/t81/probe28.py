import runpy, struct, math, collections
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
f32 = lambda b,o: struct.unpack_from('<f', b, o)[0]
rc=m['load_payload']('client',2); H,S,n=14,43,56293
lat=[f32(rc,H+j*S+1) for j in range(n)]; lon=[f32(rc,H+j*S+5) for j in range(n)]
cnti=[u32(rc,H+j*S+10) for j in range(n)]
g=collections.defaultdict(list)
for j,v in enumerate(cnti):
    if v<300: g[v].append(j)
def cent(idx):
    return (sum(lat[i] for i in idx)/len(idx), sum(lon[i] for i in idx)/len(idx))
for k in (139,55,45,76,100):
    if k in g:
        c=cent(g[k]); print(f'Cnti={k} cities={len(g[k])} centroid=({c[0]:.2f},{c[1]:.2f})')
print()
# also check Cnti is dense: which ordinals present
print('distinct Cnti',len(g),'max',max(g))
print('missing ordinals 0..250:', [i for i in range(251) if i not in g][:20])
