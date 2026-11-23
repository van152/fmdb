import importlib.util,struct,collections
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw=m.load_payload('server',6); n=m.u32(raw,8); S=40; nb=27
print('n',n,'S',S,'nb',nb)
rows=[raw[14+j*S:14+j*S+nb] for j in range(n)]
# 1. icla/iscl parent-child consistency
pair=collections.defaultdict(set)
for r in rows: pair[r[0]].add(r[1])
print('icla->iscl children per parent:', {k:sorted(v) for k,v in sorted(pair.items())})
# reverse: is each iscl under exactly one icla?
rev=collections.defaultdict(set)
for r in rows: rev[r[1]].add(r[0])
print('iscl->icla parents, multi-parent count:', sum(1 for v in rev.values() if len(v)>1), 'of', len(rev))
# 2. f32 detection at each offset
for o in range(nb-3):
    vals=[struct.unpack_from('<f',r,o)[0] for r in rows]
    fin=sum(1 for v in vals if v==v and abs(v)<1e30)
    if fin==n:
        print(f'  f32@{o}: min={min(vals):.6g} max={max(vals):.6g} distinct={len(set(vals))}')
