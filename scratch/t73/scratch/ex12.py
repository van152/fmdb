import runpy, sys, struct, time
sys.argv=['x']
dump = runpy.run_path('scripts/fm24_dump.py', run_name='notmain')
codec = dump['_reader']()
t0=time.time()
def triples(b,n):
    pts={}
    for k in range(4):
        m=(len(b)-k)//4
        for i in range(1,m-1):
            u=struct.unpack_from('<I',b,k+4*i+4)[0]
            if u==0: continue
            o=struct.unpack_from('<I',b,k+4*i)[0]
            if o>=n: continue
            v=struct.unpack_from('<I',b,k+4*i+8)[0]
            if v!=u: continue
            pts.setdefault(o,[]).append(k+4*i)
    return pts
for arch,tid in [('client',2),('client',5),('server',5),('client',19),('server',19)]:
    b=dump['load_payload'](codec,arch,tid); n=struct.unpack_from('<I',b,8)[0]
    p=triples(b,n)
    print(arch,tid,'n',n,'groups',len(p),'total pts',sum(len(v) for v in p.values()),'max/group',max((len(v) for v in p.values()),default=0),'t',round(time.time()-t0,2))
    # print positions for first few ordinals
    for o in sorted(p)[:3]:
        print('   ord',o,[hex(x) for x in p[o]][:8])
