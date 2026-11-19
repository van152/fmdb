import json, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import importlib.util
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
hits=json.loads(Path("scratch/t10/proto/hits.json").read_text())
hits.sort()
byoff={o:c for o,c in hits}
offs=set(byoff)
# disassemble small window after each hit, collect direct branch targets that land on another hit offset
edges=collections.defaultdict(set)
JCC={"je","jz","jne","jnz","jle","jg","jl","jge","ja","jae","jb","jbe","js","jns","jo","jno","jp","jnp"}
leaf=0
for o,c in hits:
    va=pe.f2va(o)
    ins=list(md.disasm(raw[o:o+0x18], va))
    for x in ins[1:]:
        if x.mnemonic in JCC or x.mnemonic=="jmp":
            try: t=int(x.op_str.strip(),0)
            except ValueError: continue
            tf=pe.va2f(t)
            if tf is not None and tf in offs:
                edges[o].add(tf)
# union find
parent={o:o for o in offs}
def find(x):
    while parent[x]!=x:
        parent[x]=parent[parent[x]]; x=parent[x]
    return x
def union(a,b):
    ra,rb=find(a),find(b)
    if ra!=rb: parent[rb]=ra
for a,bs in edges.items():
    for b in bs: union(a,b)
comp=collections.defaultdict(list)
for o in offs: comp[find(o)].append(o)
sizes=sorted((len(v) for v in comp.values()),reverse=True)
print('components',len(comp))
print('top sizes',sizes[:20])
print('sizes>=20',sum(1 for s in sizes if s>=20))
big=sorted(comp.items(), key=lambda kv:-len(kv[1]))[:8]
for r,v in big:
    v.sort()
    cs=[byoff[o] for o in v]
    print(f'component @ {v[0]:#x}..{v[-1]:#x} n={len(v)} sample={cs[:8]}')
