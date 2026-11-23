import importlib.util,collections
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw=m.load_payload('server',6); n=115; S=40
c=lambda o:[raw[14+j*S+o] for j in range(n)]
print('off10==off11:',c(10)==c(11))
print('off9==off10:',c(9)==c(10),'off9==off11:',c(9)==c(11))
for o in (2,6,9,10,11,22):
    print(f'off{o} ones={sum(c(o))}')
# iscl multi-parent
r=m.load_payload('client',6)
rows=[r[14+j*16:14+j*16+3] for j in range(n)]
par=collections.defaultdict(set)
for b in rows: par[b[1]].add(b[0])
print('multi-parent iscl:',{k:sorted(v) for k,v in par.items() if len(v)>1})
print('icla values:',sorted({b[0] for b in rows}))
print('pairs:',len({(b[0],b[1]) for b in rows}),'rows',n)
