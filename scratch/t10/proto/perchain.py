import json, collections, importlib.util
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default()
spec2 = importlib.util.spec_from_file_location("_b","scratch/t07/out/build.py")
b = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(b)
hits, md = b.decode_cmp_hits(pe); hits.sort()
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
clubs={f['code'] for f in si['entities']['club']['fields'] if f['parent'] is None}
CH={'A':(0xe82afc,0xe846ac),'B':(0xe89a34,0xe8cded),'S':(0xe57de0,0xe59000)}
for name,(lo,hi) in CH.items():
    sub=[h for h in hits if lo<=h[0]<hi]
    recs=b.find_candidates(pe, sub, md)
    codes={h[1] for h in sub}
    got={r['code'] for r in recs}
    print(f"[{name}] {lo:#x}..{hi:#x} hits={len(sub)} codes={len(codes)} clubcodes={len(codes&clubs)} resolved={len(got)} rate={len(got)/len(codes):.1%}")
    tri=sorted({(r['code'],r['object_off'],r['size']) for r in recs})
    for t in tri: print('    ',t[0],hex(t[1]),t[2])
