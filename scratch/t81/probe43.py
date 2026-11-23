import importlib.util,struct,collections
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
SPEC={6:{'client':16,'server':40},23:{'client':14,'server':14},35:{'client':15,'server':15}}
print('--- footer flag criterion: for each H in 0..16 with F=len-H-n*S, read footer as [BE u32][u32]')
for tid,dd in SPEC.items():
    for a,S in dd.items():
        raw=m.load_payload(a,tid); n=m.u32(raw,8); L=len(raw)
        ok=[]
        for H in range(0,17):
            F=L-H-n*S
            if F<=0: continue
            flag=int.from_bytes(raw[L-F:L-F+4],'big') if F>=8 else None
            lastuid=m.u32(raw,14+(n-1)*S+S-13+4) if H==14 else None
            ok.append((H,F,flag))
        print(f't{tid}/{a} L={L} n={n} S={S}')
        for H,F,flag in ok:
            tag=''
            if F>=8:
                tail=raw[len(raw)-F:len(raw)-F+4]
                v=int.from_bytes(raw[len(raw)-F+4:len(raw)-F+8],'little')
                tag=f' flagBE={int.from_bytes(tail,"big")} val={v}'
            print(f'   H={H:2d} F={F:3d}{tag}')
