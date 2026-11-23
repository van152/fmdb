import json, collections
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
ent={k:set(f['code'] for f in v['fields']) for k,v in si['entities'].items()}
clubs=ent['club']
# how many club codes appear in >=2 entities
multi={c:[k for k,s in ent.items() if c in s] for c in clubs}
n2=[c for c,v in multi.items() if len(v)>1]
print('club codes shared with other entities:',len(n2),f'{len(n2)/len(clubs):.1%}')
print('examples',n2[:12])
t4=json.load(open('scratch/t07/out/4cc_table.json',encoding='utf-8'))['codes']
# For shared codes, show candidate offsets from global table
for c in ('Cnti','Clri','Cnam','Csnm','Crep'):
    print(c,'entities',multi.get(c),'table',[(r['object_off'],r['file_off']) for r in t4.get(c,[])])
# hot-offset concentration in chain leaves
