import importlib.util
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
SPEC={6:{'client':16,'server':40},23:{'client':14,'server':14},35:{'client':15,'server':15}}
for tid,dd in SPEC.items():
    for a,S in dd.items():
        raw=m.load_payload(a,tid); n=m.u32(raw,8); L=len(raw)
        hits=[]
        for H in range(0,17):
            F=L-H-n*S
            if F<1: continue
            ok=all(m.u32(raw,H+j*S+S-13)==j and m.u32(raw,H+j*S+S-9)==m.u32(raw,H+j*S+S-5)!=0 for j in range(n))
            if ok:
                flag=int.from_bytes(raw[L-F:L-F+4],'big') if F>=8 else None
                hits.append((H,F,flag))
        print(f't{tid}/{a} L={L} n={n} S={S} alias_hits={hits}')
