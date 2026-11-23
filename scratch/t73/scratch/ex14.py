import runpy, sys, struct, collections
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
def probe(arch,tid,n,S,F,tag):
    raw=dump['load_payload'](codec,arch,tid)
    h=len(raw)-n*S-F
    print(f'===== {arch} {tid}: len={len(raw)} n={n} S={S} -> header={h} footer={F}')
    print('  header hex',raw[:h].hex(),'footer hex',raw[h+n*S:].hex())
    pos=[]
    for i in range(n):
        b=h+i*S; row=raw[b:b+S]
        for p in range(0,S-11):
            j,u,v=struct.unpack_from('<III',row,p)
            if j==i and u==v and u!=0: pos.append(p)
    print('  absolute identity triple offsets (all rows match):',sorted(set(pos)))
    # trailing bytes distinct
    for p in range(S-16,S):
        vs=collections.Counter(raw[h+i*S+p] for i in range(n))
        print(f'   byte[{p}] top3',vs.most_common(3), 'distinct',len(vs))
probe('client',2,56293,43,8,'city')
probe('client',5,7,34,8,'cont')
probe('server',5,7,48,8,'cont')
probe('client',19,28,45,8,'regi')
probe('server',19,28,46,8,'regi')
