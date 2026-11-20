import runpy, sys, struct
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
def clean(arch,tid,n,S,F):
    raw=dump['load_payload'](codec,arch,tid)
    H=len(raw)-n*S-F
    print(f'===== {arch} {tid}: len={len(raw)} H={H} S={S} F={F}')
    print('  header:', raw[:H].hex())
    print('  footer:', raw[H+n*S:].hex())
    for i in range(min(n,3)):
        b=H+i*S
        print(f'  row{i} (' + ' '.join(f'{j:02d}:{raw[b+j]:02x}' for j in range(S)) + ')')
    # find identity triple column matching all rows
    for p in range(0,S-11):
        ok=sum(1 for i in range(n) if struct.unpack_from('<III',raw,H+i*S+p)[0]==i and
               struct.unpack_from('<III',raw,H+i*S+p)[1]==struct.unpack_from('<III',raw,H+i*S+p)[2]!=(0,)) if False else None
    hits=[]
    for p in range(0,S-11):
        good=0
        for i in range(n):
            j,u,v=struct.unpack_from('<III',raw,H+i*S+p)
            if j==i and u==v and u!=0: good+=1
        if good==n: hits.append(p)
        elif good: hits.append((p,good))
    print('  identity col:',hits)
clean('client',5,7,34,8)
clean('server',5,7,48,8)
clean('client',19,28,45,8)
clean('server',19,28,46,8)
clean('client',2,56293,43,8)
