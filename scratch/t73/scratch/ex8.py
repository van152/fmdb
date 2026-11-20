import runpy, sys, struct
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
def probe(arch,tid,n,S,T):
    raw=dump['load_payload'](codec,arch,tid)
    print(f'--- {arch} {tid} n={n} S={S} len={len(raw)}')
    for h in range(0,25):
        if len(raw)-h-n*S!=0 and (len(raw)-h-n*S) not in (7,8,9,10,12): continue
        F=len(raw)-h-n*S
        ok=0;pe=0;nz=0
        for i in range(n):
            a=h+i*S+S-T
            if a<0 or a+12>len(raw): break
            j,u,v=struct.unpack_from('<III',raw,a)
            ok+= (j==i); pe+= (u==v); nz+= (u!=0)
        print(f'  h={h} F={F} id@{n} T={T}: ordinal_ok={ok} pair={pe} nonzero={nz}')
probe('client',2,56293,43,13)
probe('client',5,7,34,13)
probe('server',5,7,48,12)
probe('client',19,28,45,13)
probe('server',19,28,46,12)
