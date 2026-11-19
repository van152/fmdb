import json, collections, importlib.util
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default()
spec2 = importlib.util.spec_from_file_location("_b","scratch/t07/out/build.py")
b = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(b)
hits, md = b.decode_cmp_hits(pe); hits.sort()
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
club=[f['code'] for f in si['entities']['club']['fields'] if f['parent'] is None]
clubs=set(club); cluball={f['code'] for f in si['entities']['club']['fields']}
t4=json.load(open('scratch/t07/out/4cc_table.json',encoding='utf-8'))['codes']
anchor=clubs&set(t4)
GAP=0x200
cl=[]; cur=[hits[0]]
for h in hits[1:]:
    if h[0]-cur[-1][0]<=GAP: cur.append(h)
    else: cl.append(cur); cur=[h]
cl.append(cur)
big=[c for c in cl if len(c)>=20]
print('total clusters',len(cl),'n>=20 clusters',len(big))
cov=set()
for c in big: cov|={h[1] for h in c}
clubhit={h[1] for h in hits} & clubs
print('club codes with any cmp hit',len(clubhit))
print('  inside n>=20 clusters',len(clubhit&cov),f'{len(clubhit&cov)/len(clubhit):.1%}')
print('  outside',len(clubhit-cov))
# rank chains by club overlap
rank=[]
for c in big:
    cs={h[1] for h in c}
    rank.append((len(cs&clubs), len(cs&anchor), len(cs), c[0][0], c[-1][0]))
rank.sort(reverse=True)
print(f"{'clubOv':>6} {'anchorOv':>8} {'n':>4} range")
for r in rank[:10]: print(f"{r[0]:>6} {r[1]:>8} {r[2]:>4} {r[3]:#x}..{r[4]:#x}")
# chains with anchor overlap > 0
print('chains with anchor overlap>0:',sum(1 for r in rank if r[1]>0))
