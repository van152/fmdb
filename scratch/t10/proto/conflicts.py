import json
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
clubs={f['code'] for f in si['entities']['club']['fields'] if f['parent'] is None}
t4=json.load(open('scratch/t07/out/4cc_table.json',encoding='utf-8'))['codes']
best={}
for c in clubs:
    for r in t4.get(c,[]):
        if c not in best or r['score']>best[c]['score']: best[c]=r
slots={}
for c,r in best.items(): slots.setdefault(r['object_off'],[]).append((c,r['size'],r['file_off'],r['kind']))
ks=sorted(slots)
print('distinct offsets',len(ks),'span',hex(ks[0]),hex(ks[-1]))
bad=0
for a,b in zip(ks,ks[1:]):
    sa=max(s for _,s,_,_ in slots[a])
    if a+sa>b:
        bad+=1
        print(f'  OVERLAP {hex(a)}+{sa} > {hex(b)}   A={[x[0] for x in slots[a]]}  B={[x[0] for x in slots[b]]}')
print('overlaps',bad,'of',len(ks)-1)
for k in ks: print(f'  {k:#5x} size={max(s for _,s,_,_ in slots[k])} codes={[x[0] for x in slots[k]][:6]} n={len(slots[k])}')
