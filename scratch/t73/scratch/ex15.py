import runpy, sys, struct
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()

def scan(arch,tid,n,S):
    raw=dump['load_payload'](codec,arch,tid)
    print(f'===== {arch} {tid} len={len(raw)} n={n} S={S}')
    for F in (7,8,9,10,12):
        h=len(raw)-n*S-F
        if h<0: continue
        # exact triple per row at fixed p
        best={}
        for p in range(0,S-12):
            c12=c13=0
            for i in range(n):
                b=h+i*S+p
                if b+13>len(raw): break
                j,u,v=struct.unpack_from('<III',raw,b)
                if j==i and u==v and u!=0:
                    c12+=1
                    if raw[b+12]==0: c13+=1
            if c12: best[p]=(c12,c13)
        print(f'  F={F} h={h}: '+', '.join(f'p={p}:12B {v[0]}/{n} 13B {v[1]}/{n}' for p,v in sorted(best.items())))
scan('client',2,56293,43)
scan('client',5,7,34)
scan('server',5,7,48)
scan('client',19,28,45)
scan('server',19,28,46)
