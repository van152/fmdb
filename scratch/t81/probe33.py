import importlib.util,re
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for tid in (6,23,35):
    for a in ('client','server'):
        raw=m.load_payload(a,tid)
        strs=[(i,s.decode()) for i,s in ((mo.start(),mo.group()) for mo in re.finditer(rb'[ -~]{3,}',raw))]
        print(f'== t{tid}/{a} L={len(raw)} strings={len(strs)}')
        for i,s in strs[:8]: print('   ',i,repr(s[:70]))
        if len(strs)>8: print('    ... last', strs[-1][0], repr(strs[-1][1][:70]))
