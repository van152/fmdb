import importlib.util,collections
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw=m.load_payload('server',6); n=115; S=40; nb=27
rows=[raw[14+j*S:14+j*S+nb] for j in range(n)]
f=[r[2] for r in rows]
print('off2 ones',sum(f))
for o in range(nb):
    v=[r[o] for r in rows]
    eq=sum(1 for a,b in zip(f,v) if a==b)
    if eq>100 and o!=2: print(f'  col{o} matches off2 {eq}/115 vals={sorted(set(v))}')
print('crosstab off2 x off0:', collections.Counter((r[0],r[2]) for r in rows))
# which rows have off2=1 -> check off16 (56..65) and off20/21
print('ones rows detail (off0,off1,off2,off16,off20,off21,off22,off23):')
for j in range(n):
    if f[j]: print('  ',j,[rows[j][o] for o in (0,1,2,16,20,21,22,23)])
