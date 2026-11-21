import json,sys,struct
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
for arch,size in (('client',83927),('server',105228)):
    rows=[json.loads(l) for l in open(f'scratch/t50/out/profiles/table_{arch}_extra_9.rows.jsonl',encoding='utf-8')]
    raw=C.payload(arch,f'{arch}_db/table_extra_9.dat',size)
    print('==',arch,'rows',len(rows),'payload',len(raw))
    starts=[r['offset'] for r in rows]; lens=[r['len'] for r in rows]
    print(' starts[:5]',starts[:5],'sum',sum(lens),'hdr',starts[0])
    for i in (0,1,2,3,139):
        o,l=starts[i],lens[i]
        b=raw[o:o+l]
        print(f' row{i} off={o} len={l} head={b[:28].hex(" ")} tail={b[-20:].hex(" ")}')
