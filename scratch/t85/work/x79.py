import sys,json
sys.path.insert(0,'scripts'); sys.stdout.reconfigure(encoding='utf-8')
import t85_common as C
print('%-38s %10s %6s %8s %8s'%('member','payload','251','7047','both'))
for arch in ('client','server'):
    ents,_=C.entries(arch)
    for e in ents:
        if e.get('entry_type')!='table': continue
        n=int(e['size'])
        if n%251==0 or n%7047==0:
            print('%-38s %10d %6s %8s'%(f'{arch}/{e["path"].split("/")[-1]}',n,n%251==0,n%7047==0))
