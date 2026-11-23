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
byoff={h[0]:h[1] for h in hits}; offs=set(byoff); hmap={h[0]:h for h in hits}
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
ent={k:{f['code'] for f in v['fields']} for k,v in si['entities'].items()}
JCC={"je","jz","jne","jnz","jle","jg","jl","jge","ja","jae","jb","jbe","js","jns","jo","jno","jp","jnp"}
edges=collections.defaultdict(set)
for o,c,*_ in hits:
    va=pe.f2va(o)
    for x in list(md.disasm(pe.raw[o:o+0x18], va))[1:]:
        if x.mnemonic in JCC or x.mnemonic=="jmp":
            try: t=int(x.op_str.strip(),0)
            except ValueError: continue
            tf=pe.va2f(t)
            if tf is not None and tf in offs: edges[o].add(tf)
parent={o:o for o in offs}
def find(x):
    while parent[x]!=x: parent[x]=parent[parent[x]]; x=parent[x]
    return x
for a,bs in edges.items():
    for c in bs:
        ra,rb=find(a),find(c)
        if ra!=rb: parent[rb]=ra
comp=collections.defaultdict(list)
for o in offs: comp[find(o)].append(o)
rows=[]
for r,v in comp.items():
    if len(v)<20: continue
    v.sort(); cs=[byoff[o] for o in v]
    subhits=[hmap[o] for o in v]
    recs=b.find_candidates(pe, subhits, md)
    got={x['code'] for x in recs}
    ov={k:len(set(cs)&s) for k,s in ent.items()}
    best=max(ov.items(), key=lambda kv:kv[1])
    rows.append(dict(n=len(v),start=hex(v[0]),end=hex(v[-1]),club=ov['club'],
                     distinct=len(set(cs)), named=len(got), best=best[0], bestn=best[1], cs=cs[:8]))
rows.sort(key=lambda r:-r['n'])
print(f"{'n':>4} {'start':>9} {'end':>9} {'club':>4} {'named':>5} {'rate':>6} best")
for r in rows:
    print(f"{r['n']:>4} {r['start']:>9} {r['end']:>9} {r['club']:>4} {r['named']:>5} {r['named']/r['n']:>5.1%} {r['best']}:{r['bestn']}  {r['cs'][:4]}")
Path('scratch/t10/proto/compstats.json').write_text(json.dumps(rows,ensure_ascii=False,indent=1),encoding='utf-8')
