import importlib.util,struct
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for tid in (6,23,35):
    for a in ('client','server'):
        raw=m.load_payload(a,tid); n=m.u32(raw,8)
        print(f'== t{tid}/{a} L={len(raw)} n={n}')
        print('   hdr14:', raw[:14].hex(' '))
        print('   footer8:', raw[-8:].hex(' '))
        print('   tail 64:', raw[-64:].hex(' '))
