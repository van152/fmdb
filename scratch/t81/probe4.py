import runpy, struct, collections, json
m = runpy.run_path('scripts/t73_mapper_core.py', run_name='x')
u32 = lambda b,o: struct.unpack_from('<I', b, o)[0]
raw = m['load_payload']('server',6); n=u32(raw,8); S=40; p=27
print('n',n,'L',len(raw))
for off in range(S-13):
    c8=[raw[14+j*S+off] for j in range(n)]
    b=bytes(c8)
    d={}
    for w in (1,2):
        v=[int.from_bytes(b[i:i+w],'little') for i in range(len(b)-w+1)]
        d['u%d'%(8*w)]=(min(v),max(v),len(set(v)))
    f=[struct.unpack_from('<f',b,i)[0] for i in range(len(b)-3)]
    d['f32']=(round(min(f),4),round(max(f),4))
    print(off, d, 'top', collections.Counter(c8).most_common(3))
