import runpy, sys, struct
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
def idx(bs, base=0):
    return ' '.join(f'{base+i:02d}:{b:02x}' for i,b in enumerate(bs))
for arch,tid,n,S,T in [('client',5,7,34,13),('server',5,7,48,12),('client',19,28,45,13),('server',19,28,46,12)]:
    raw=dump['load_payload'](codec,arch,tid)
    print(f'===== {arch} {tid} stride {S} T {T}')
    for i in range(n if n<8 else 4):
        b=h=13+i*S
        row=raw[h:h+S]
        print(f' row{i}:', row.hex())
        print('   ', ' '.join(f'{j:02d}:{x:02x}' for j,x in enumerate(row)))
    # identity position check
    triples=set()
    for i in range(n):
        for p in range(0,S-11):
            a=13+i*S+p
            j,u,v=struct.unpack_from('<III',raw,a)
            if j==i and u==v and u!=0: triples.add(p)
    print('  identity offsets matching (ordinal,uid,uid) all rows:',sorted(triples))
