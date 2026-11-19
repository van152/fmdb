import json, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import importlib.util
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
hits=json.loads(Path("scratch/t10/proto/hits.json").read_text()); hits.sort()
byoff={o:c for o,c in hits}; offs=set(byoff)
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
ent={k:{f['code'] for f in v['fields']} for k,v in si['entities'].items()}
JCC={"je","jz","jne","jnz","jle","jg","jl","jge","ja","jae","jb","jbe","js","jns","jo","jno","jp","jnp"}
edges=collections.defaultdict(set)
for o,c in hits:
    va=pe.f2va(o)
    for x in list(md.disasm(raw[o:o+0x18], va))[1:]:
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
    for b in bs:
        ra,rb=find(a),find(b)
        if ra!=rb: parent[rb]=ra
comp=collections.defaultdict(list)
for o in offs: comp[find(o)].append(o)
club=ent['club']
rows=[]
for r,v in comp.items():
    if len(v)<20: continue
    v.sort(); cs=[byoff[o] for o in v]
    ov=len(set(cs)&club)
    best=max(((len(set(cs)&s),k) for k,s in ent.items() if k!='club'), default=(0,''))
    rows.append((len(v),v[0],v[-1],ov,best,cs[:6],len(set(cs))))
rows.sort(reverse=True)
print(f"{'n':>4} {'start':>9} {'end':>9} {'clubOv':>6} {'distinct':>8} best_entity  sample")
for n,a,b,ov,best,cs,nd in rows[:25]:
    print(f"{n:>4} {a:#9x} {b:#9x} {ov:>6} {nd:>8} {best[1]}:{best[0]:<4} {cs[:5]}")
