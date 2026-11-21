import importlib.util
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
a=m.load_payload('client',6); b=m.load_payload('server',6)
print('client len',len(a),'server len',len(b),'same?',a==b)
# correct stride anchors
for tid,S in ((6,16),(6,40)):
    pass
for a_,tid,S in (('client',6,16),('server',6,40),('client',23,14),('server',23,14),('client',35,15),('server',35,15)):
    raw=m.load_payload(a_,tid); n=m.u32(raw,8)
    ro=S-13
    ok=sum(1 for j in range(n) if m.u32(raw,14+j*S+ro)==j)
    oku=sum(1 for j in range(n) if m.u32(raw,14+j*S+ro+4)==m.u32(raw,14+j*S+ro+8)!=0)
    print(f't{tid}/{a_} S={S} rdui@{ro} ord_ok={ok}/{n} duni@{ro+4} uid_ok={oku}/{n}')
