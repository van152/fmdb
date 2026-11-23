import importlib.util,struct,collections,json
spec=importlib.util.spec_from_file_location('m','scripts/t81_fk_index.py'); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
raw=m.load_payload('server',6); n=115; S=40; nb=27
rows=[raw[14+j*S:14+j*S+nb] for j in range(n)]
f=[struct.unpack_from('<f',r,13)[0] for r in rows]
print('Iocr f32@13: min',min(f),'max',max(f),'distinct',len(set(f)))
print(' vals:',sorted(set(f))[:14])
print(' byte16 set:',sorted({r[16] for r in rows}))
for off in (7,17,24,20,25,26,23,21,8,2,9,10,11,22,12,18):
    v=[r[off] for r in rows]
    print(f'off{off}: distinct={len(set(v))} vals={sorted(set(v))} counts={collections.Counter(v).most_common(5)}')
b18=[int.from_bytes(r[18:20],'little') for r in rows]
print('u16@18:',min(b18),max(b18),'distinct',len(set(b18)),'all<8192:',all(x<8192 for x in b18))
print('bits used:',sorted({1<<k for x in b18 for k in range(16) if x>>k&1}))
print('Icau 13-bit cap 0x1FFF covers all:',all(x<=0x1FFF for x in b18))
