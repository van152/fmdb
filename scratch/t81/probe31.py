import sys,struct,importlib.util
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
for tid,S in [(6,None),(23,None),(35,None)]:
    for a in ('client','server'):
        raw=m.load_payload(a,tid); n=m.u32(raw,8); L=len(raw)
        stride=(L-14-8)//n
        print(f'== t{tid}/{a} L={L} n={n} stride={(L-22)/n} int_stride={stride}')
        for j in range(min(4,n)):
            s=14+j*stride
            print('   ',j,raw[s:s+stride].hex(' '))
