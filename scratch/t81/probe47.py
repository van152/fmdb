import importlib.util,collections
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
c=m.load_payload('client',6); s=m.load_payload('server',6); n=115
cb=[c[14+j*16+2] for j in range(n)]
print('client byte2 ones',sum(cb),'rows',[j for j in range(n) if cb[j]])
print('--- client byte2 vs server col equality (100..114):')
for k in range(27):
    col=[s[14+j*40+k] for j in range(n)]
    eq=sum(1 for a,b in zip(cb,col) if a==b)
    if eq>=100: print(f'   server col{k} eq={eq} vals={sorted(set(col))}')
print('--- Irec(server off8) vs client byte2 crosstab:',collections.Counter((s[14+j*40+8],cb[j]) for j in range(n)))
print('--- server off9..12,22 vs off2 crosstab')
for k in (9,10,11,12,22,6,20):
    print(f'   col{k}:',collections.Counter((s[14+j*40+k],cb[j]) for j in range(n)))
# t23 uid structure
r=m.load_payload('client',23); nn=m.u32(r,8)
u=[m.u32(r,14+j*14+9) for j in range(nn)]
small=[x for x in u if x<10000]
print('t23 uids small',len(small),'min',min(u),'gaps',[k for k in range(1,280) if k not in set(u)][:20])
print('t23 rows 0..3 raw', [r[14+j*14:14+j*14+14].hex() for j in range(3)])
