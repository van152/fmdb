import importlib.util
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for tid,S,nb in ((6,40,27),(23,14,1),(35,15,2)):
    raw=m.load_payload('client',tid); n=m.u32(raw,8)
    uids=[m.u32(raw,14+j*S+S-13+4) for j in range(n)]
    seq=[j for j in range(n) if uids[j]==j+1]
    print(f't{tid}: rows with uid==j+1: {len(seq)}/{n}')
    first_break=next((j for j in range(n) if uids[j]!=j+1),None)
    print('   first break at row',first_break,'uid',uids[first_break] if first_break is not None else None)
    print('   tail uids',uids[-3:])
# popcount for Icau candidate
raw=m.load_payload('server',6); n=115
v=[int.from_bytes(raw[14+j*40+18:14+j*40+20],'little') for j in range(n)]
print('Icau u16 popcount hist',{k:v.count(k) for k in sorted({bin(x).count("1") for x in v})})
print('values',sorted(set(v)))
print('hi byte',sorted({x>>8 for x in v}),'lo byte',sorted({x&0xff for x in v})[:20])
