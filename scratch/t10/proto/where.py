import json, collections, importlib.util
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default()
spec2 = importlib.util.spec_from_file_location("_b","scratch/t07/out/build.py")
b = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(b)
hits, md = b.decode_cmp_hits(pe); hits.sort()
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
club=[f for f in si['entities']['club']['fields'] if f['parent'] is None]
clubs={f['code'] for f in club}
ch=[h for h in hits if h[1] in clubs]
print('club cmp hits',len(ch),'distinct codes',len({h[1] for h in ch}))
r=collections.Counter(h[0]//0x1000*0x1000 for h in ch)
print('top 0x1000 pages by hit count (club codes only):')
for k,v in r.most_common(15): print(f'   {k:#x}  {v}  codes={len({h[1] for h in ch if h[0]//0x1000*0x1000==k})}')
# which codes never in A or B
def inrange(h,a,c): return a<=h[0]<c
A=set(h[1] for h in ch if inrange(h,0xe82afc,0xe846ac))
B=set(h[1] for h in ch if inrange(h,0xe89a34,0xe8cded))
rest=clubs-A-B
print('club codes not in A∪B:',len(rest))
rr=collections.Counter()
for h in ch:
    if h[1] in rest: rr[h[0]//0x10000*0x10000]+=1
print('their file_off 64K buckets:',[(hex(k),v) for k,v in rr.most_common(10)])
# for those rest, how many appear in any chain with >=20
