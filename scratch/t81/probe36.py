import importlib.util,hashlib
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
SPEC={6:{'client':16,'server':40},23:{'client':14,'server':14},35:{'client':15,'server':15}}
for tid,dd in SPEC.items():
    print(f'== t{tid}')
    raws={}
    for a,S in dd.items():
        raw=m.load_payload(a,tid); raws[a]=raw
        print(f'   {a} len={len(raw)} sha={hashlib.sha256(raw).hexdigest()[:16]} hdr={raw[:14].hex(" ")}')
    print('   payload identical:', raws['client']==raws['server'])
    # prefix comparison
    for a,S in dd.items():
        raw=raws[a]; n=m.u32(raw,8); nb=S-13
        print(f'   {a} biz_prefix={raw[14:14+min(nb,6)].hex(" ")} n={n}')
# cross-archive column match for t6 (biz widths differ)
rawc=m.load_payload('client',6); raws=m.load_payload('server',6)
n=115; bc=3; bs=27
cc=[[rawc[14+j*16+k] for j in range(n)] for k in range(bc)]
sc=[[raws[14+j*40+k] for j in range(n)] for k in range(bs)]
print('== t6 cross-archive u8 column equality (client col vs server col)')
for i in range(bc):
    best=[(j,sum(1 for a,b in zip(cc[i],sc[j]) if a==b)) for j in range(bs)]
    best.sort(key=lambda t:-t[1])
    print(f'   client off{i} -> server off{best[0][0]} match {best[0][1]}/115; runner-up off{best[1][0]} {best[1][1]}/115')
