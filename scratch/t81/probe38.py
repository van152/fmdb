import importlib.util,json,collections
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
M=json.load(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8'))
en={k:set(int(v['enum']) for v in M['enums'][k]['values']) for k in ('icla','iscl','Icau','inSr','Iagr','Icms')}
raw=m.load_payload('server',6); n=115; S=40; nb=27
biz=[raw[14+j*S:14+j*S+nb] for j in range(n)]
for o in range(nb):
    vals=[b[o] for b in biz]
    s=set(vals)
    hit=[k for k,v in en.items() if s<=v]
    print(f'off{o:2d} n={len(s):3d} min={min(vals):3d} max={max(vals):3d} enum_subset={hit} vals={sorted(s)[:12]}')
