import sys,struct,json
sys.path.insert(0,'scratch/t85/work'); sys.stdout.reconfigure(encoding='utf-8')
import common as C
res={}
for arch in ('client','server'):
    ents,_=C.entries(arch)
    for e in ents:
        if e.get('entry_type')!='table': continue
        raw=C.payload(arch,e['path'],int(e['size']))
        # identity-based 251 rows?
        n=0
        for i in range(0,len(raw)-13):
            a,b,c=struct.unpack_from('<III',raw,i)
            if b==c and raw[i+12]==0 and a==n: n+=1
        res[(arch,e['path'])]={'payload':len(raw),'ident':n}
        if n in (251,) or (n>100 and n%251==0):
            print(f'HIT {arch:6s} {e["path"]:34s} payload={len(raw):9d} rows={n}')
json.dump({f'{a}|{b}':v for (a,b),v in res.items()},open('scratch/t85/work/scan251.json','w'),indent=1)
