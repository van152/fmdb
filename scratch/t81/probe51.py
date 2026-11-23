import importlib.util
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for tid,a,S in ((6,'client',16),(6,'server',40),(23,'client',14),(35,'client',15)):
    raw=m.load_payload(a,tid); n=m.u32(raw,8)
    uids=[m.u32(raw,14+j*S+S-13+4) for j in range(n)]
    seq=sum(1 for j in range(n) if uids[j]==j+1)
    fb=next((j for j in range(n) if uids[j]!=j+1),None)
    print(f't{tid}/{a}: uid==j+1 {seq}/{n} first_break={fb} tail={uids[-3:]}')
raw=m.load_payload('server',6); n=115
v=[int.from_bytes(raw[14+j*40+18:14+j*40+20],'little') for j in range(n)]
print('Icau u16 popcount hist',{k:v.count(k) for k in sorted({bin(x).count('1') for x in v})})
print('values',sorted(set(v)))
print('hi',sorted({x>>8 for x in v}),'lo',sorted({x&0xff for x in v}))
