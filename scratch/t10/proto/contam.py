import json, collections
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
ent={k:set(f['code'] for f in v['fields']) for k,v in si['entities'].items()}
clubs=ent['club']
t4=json.load(open('scratch/t07/out/4cc_table.json',encoding='utf-8'))['codes']
cand=[c for c in clubs if c in t4]
print('club codes with table candidate',len(cand))
# source page of the best record
pages=collections.Counter()
for c in cand:
    for r in t4[c]:
        pages[r['file_off'][:6] if isinstance(r['file_off'],str) else '?']+=1
def region(fo):
    o=int(fo,16)
    if 0xe54c00<=o<0xe55f00: return 'city_reader_0xe55xxx'
    if 0xe82afc<=o<0xe846ac: return 'chainA'
    if 0xe89a34<=o<0xe8cded: return 'chainB'
    if 0xe57de0<=o<0xe59000: return 'chainS'
    return 'other'
tot=collections.Counter()
bestreg=collections.Counter()
for c in cand:
    regs={region(r['file_off']) for r in t4[c]}
    for x in regs: tot[x]+=1
    best=max(t4[c], key=lambda r:r['score'])
    bestreg[region(best['file_off'])]+=1
print('by best record region:',dict(bestreg))
print('any-region counts:',dict(tot))
# which of these offsets are outside 0x20..0x400
bad=[(c,r['object_off']) for c in cand for r in t4[c] if not (0x20<=r['object_off']<=0x400)]
print('records outside 0x20..0x400:',len(bad),bad[:5])
offs={r['object_off'] for c in cand for r in t4[c]}
print('distinct offsets',len(offs),'min',hex(min(offs)),'max',hex(max(offs)))
# multiplicity: same offset claimed by >1 club code
m=collections.Counter()
for c in cand:
    for o in {r['object_off'] for r in t4[c]}: m[o]+=1
print('offsets claimed by >1 club code:',sum(1 for v in m.values() if v>1),'of',len(m))
