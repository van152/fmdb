from pathlib import Path
import json, struct, sys, math
from collections import Counter
P=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(P.parent/'scripts'))
import fm24_dump as db
co=db._reader()
for a in ['client','server']:
 d=co['list_tables'](db.DB_DIR/(a+'_db.dat'),a+'_db.dat');print(a,len(d),[r for r in d if r['table_id']==33])
raw=db.load_payload(co,'server',33); print(len(raw),raw[:13].hex(),raw[-9:].hex())
p=json.loads((P/'t29/out/profiles/table_server_33.profile.json').read_bytes()); c={(i['offset'],i['width']):i for i in p['columns']}; lens=[4,4,2,4,1,4,4,4,4,1,4,4,4,4,4,4,4,1,1,4,12]
o=0
for w in lens:
 bs=[raw[k+o:k+o+w] for k in range(14,len(raw)-9,79)]; hs=Counter(int.from_bytes(b,'little',signed=True) for b in bs); print(o,w,len(hs),min(hs),max(hs),hs.most_common(10))
 if o in [19,23]:
  days=[struct.unpack('<HH',b) for b in bs];bad=[(i,x,bs[i].hex()) for i,x in enumerate(days) if not(1<=x[0]<=366 and 1850<=x[1]<=2100)]; print('dates',len(bad),bad[:10],min(y for d,y in days), max(y for d,y in days),min(d for d,y in days),max(d for d,y in days),c[o,w]['packed_day_year'])
 if o==27:
  fs=Counter(struct.unpack('<f',b)[0] for b in bs);print('float',len(fs),fs.most_common(20),min(fs),max(fs),sum(k for x,k in fs.items() if not math.isfinite(x)))
 o+=w
print(o)
