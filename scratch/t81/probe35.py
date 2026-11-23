import importlib.util,collections
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for tid,S in ((23,14),(35,15)):
    raw=m.load_payload('client',tid); n=m.u32(raw,8); nb=S-13
    uids=[m.u32(raw,14+j*S+nb+4) for j in range(n)]
    big=[(j,u) for j,u in enumerate(uids) if u>10000]
    print(f'== t{tid} n={n} big_uids={len(big)}')
    print('   small seq ok:', all(uids[j]==j+1 for j in range(min(n,5))))
    print('   big rows first 12:', big[:12])
    base=min(u for _,u in big) if big else 0
    print('   base',base,hex(base))
    print('   offsets', [u-base for _,u in big][:20])
    print('   big uid rows contiguous?', [j for j,_ in big][:20])
    # ordinal check
    ords=[m.u32(raw,14+j*S+nb) for j in range(n)]
    print('   ord ok', all(o==j for j,o in enumerate(ords)))
