import json, collections, importlib.util
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default()
spec2 = importlib.util.spec_from_file_location("_b","scratch/t07/out/build.py")
b = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(b)
hits, md = b.decode_cmp_hits(pe)
hits.sort()
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
club=[f['code'] for f in si['entities']['club']['fields'] if f['parent'] is None]
clubs=set(club)
t4=json.load(open('scratch/t07/out/4cc_table.json',encoding='utf-8'))['codes']
anchor={c for c in clubs if c in t4}
print('club codes',len(clubs),'exact in table',len(anchor))
GAP=0x200
clusters=[]; cur=[hits[0]]
for h in hits[1:]:
    if h[0]-cur[-1][0] <= GAP: cur.append(h)
    else: clusters.append(cur); cur=[h]
clusters.append(cur)
print('clusters',len(clusters))
rows=[]
for cl in clusters:
    cs=[h[1] for h in cl]
    ov=len(set(cs)&clubs); ova=len(set(cs)&anchor)
    if len(cl)>=20:
        rows.append((len(cl), cl[0][0], cl[-1][0], ov, ova, len(set(cs))))
rows.sort(reverse=True)
print(f"{'n':>4} {'start':>9} {'end':>9} {'clubOv':>6} {'anchorOv':>8} {'distinct':>8}")
for r in rows[:20]: print(f"{r[0]:>4} {r[1]:#9x} {r[2]:#9x} {r[3]:>6} {r[4]:>8} {r[5]:>8}")
