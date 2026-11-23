import importlib.util,collections
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
c=m.load_payload('client',6); s=m.load_payload('server',6); n=115
cc=[[c[14+j*16+k] for j in range(n)] for k in range(3)]
ss=[[s[14+j*40+k] for j in range(n)] for k in range(27)]
for k in range(3):
    print(f'client off{k}: {collections.Counter(cc[k]).most_common()}   eq_server_off{k}={sum(1 for a,b in zip(cc[k],ss[k]) if a==b)}')
print('server off2:', collections.Counter(ss[2]).most_common())
print('server off0:', collections.Counter(ss[0]).most_common())
print('server off1 count:', len(set(ss[1])))
print('client rows 30..40 off0,1,2:', [(cc[0][j],cc[1][j],cc[2][j]) for j in range(30,40)])
print('server rows 30..40 off0,1,2:', [(ss[0][j],ss[1][j],ss[2][j]) for j in range(30,40)])
