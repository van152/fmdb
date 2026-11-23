import importlib.util,json,collections
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
c=m.load_payload('client',6); s=m.load_payload('server',6); n=115
cc=[[c[14+j*16+k] for j in range(n)] for k in range(3)]
ss=[[s[14+j*40+k] for j in range(n)] for k in range(40)]
print('client off2 vs each server col equality:')
for k in range(27):
    e=sum(1 for a,b in zip(cc[2],ss[k]) if a==b)
    if e>=100: print(f'   off{k}: {e}/115 values={sorted(set(ss[k]))}')
print('client off2 ones rows', [j for j in range(n) if cc[2][j]==1][:30])
M=json.load(open('evidence/fm24/reports/editor_schema/master.json',encoding='utf-8'))
print('field dict sample:', json.dumps(M['entities']['injury.xml'][0]['fields'][8],ensure_ascii=False))
print()
for f in M['entities']['injury.xml'][0]['fields']:
    print(' ',f['field'],f['type'],f.get('min_value'),f.get('max_value'),'client' if f.get('is_client_field') else '')
