import json,sys
sys.stdout.reconfigure(encoding='utf-8')
c=json.loads(open('scratch/t85/work/scan251.json',encoding='utf-8').read())
print('%-42s %10s %8s  mult251 mult7047'%('member','payload','rows'))
for k,v in sorted(c.items()):
    n=v['ident']
    m251 = n%251==0 and n>0
    m7047 = n%7047==0 and n>0
    if m251 or m7047 or n in (251,7047):
        print('%-42s %10d %8d   %-5s %s'%(k,v['payload'],n,m251,m7047))
