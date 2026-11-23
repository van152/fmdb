import importlib.util,json,collections
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
M=json.load(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8'))
E={k:set(int(v['enum']) for v in M['enums'][k]['values']) for k in ('icla','iscl','Icau','inSr','Iagr','Icms')}
raw=m.load_payload('server',6); n=115; S=40
c=lambda o,w=1:[int.from_bytes(raw[14+j*S+o:14+j*S+o+w],'little') for j in range(n)]
for o in (0,1,2,4,6,7,9,10,11,12,20,21,22,23,24,25,26):
    v=c(o); s=set(v)
    print(f'off{o}: distinct={len(s)} min={min(v)} max={max(v)}')
    for k,e in E.items():
        if s<=e: print(f'    SUBSET of {k}: equal={s==(e-{-3}) or s==e} enum={sorted(e)}')
print()
print('icla observed',sorted(set(c(0))),'enum',sorted(E['icla']))
print('iscl observed n',len(set(c(1))),'enum n',len(E['iscl']),'subset',set(c(1))<=E['iscl'],'equal_minusAny',set(c(1))==E['iscl']-{-3})
print('inSr observed',sorted(set(c(23))),'enum',sorted(E['inSr']))
print('Icms observed',sorted(set(c(21))),'enum',sorted(E['Icms']))
print('Iagr observed?', sorted(set(c(20))),'enum',sorted(E['Iagr']))
print('Icau u16@18 observed',sorted(set(c(18,2))),'enum',sorted(E['Icau']))
