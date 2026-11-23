import importlib.util,json,collections,struct
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
M=json.load(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8'))
for k in ('icla','iscl'):
    print(k, [(v['enum'],v['name']) for v in M['enums'][k]['values']])
print()
print('field_codes Imio/Icdo:', M['field_codes'].get('Imio'), M['field_codes'].get('Icdo'))
raw=m.load_payload('server',6); n=115; S=40; nb=27
rows=[raw[14+j*S:14+j*S+nb] for j in range(n)]
print('--- u16 columns')
for o in range(nb-1):
    v=[int.from_bytes(r[o:o+2],'little') for r in rows]
    nn=[x for x in v if x!=0xffff]
    print(f'  u16@{o:2d} distinct={len(set(v)):3d} min={min(v):5d} max={max(v):5d} ff={v.count(0xffff)}')
