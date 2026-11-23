import json, collections
from pathlib import Path
hits = json.loads(Path("scratch/t10/proto/hits.json").read_text())
hits.sort()
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
club={f['code'] for f in si['entities']['club']['fields']}
city={f['code'] for f in si['entities']['city']['fields']}
inj={f['code'] for f in si['entities']['injury']['fields']} if 'injury' in si['entities'] else set()
print('entities keys', list(si['entities']))
def region(h, size=0x1000): return h[0]//size*size
for name,S in (('club',club),('city',city)):
    sub=[(o,c) for o,c in hits if c in S]
    print(name,'schema codes',len(S),'hits',len(sub),'distinct codes',len({c for _,c in sub}))
    r=collections.Counter(region(h) for h in sub)
    for k,v in r.most_common(15):
        print('   ',hex(k),v)
