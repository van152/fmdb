import sys,struct,collections,importlib.util
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
SPEC={6:{'client':16,'server':40},23:{'client':14,'server':14},35:{'client':15,'server':15}}
for tid,dd in SPEC.items():
    for a,S in dd.items():
        raw=m.load_payload(a,tid); n=m.u32(raw,8); nb=S-13
        biz=[raw[14+j*S:14+j*S+nb] for j in range(n)]
        print(f'== t{tid}/{a} n={n} biz={nb}')
        for o in range(nb):
            c=collections.Counter(b[o] for b in biz)
            top=c.most_common(6)
            print(f'   off{o}: distinct={len(c)} top={top}')
