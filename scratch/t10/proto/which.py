import json, collections, importlib.util
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
spec2 = importlib.util.spec_from_file_location("_b","scratch/t07/out/build.py")
b = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(b)
hits, md = b.decode_cmp_hits(pe); hits.sort()
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
ents={}
for k,v in si['entities'].items():
    ents[k]=set(f['code'] for f in v['fields'])
CL={k:s for k,s in ents.items() if k.startswith('club')}
for k,s in CL.items(): print(k,len(s))
A=[h for h in hits if 0xe82afc<=h[0]<0xe846ac]
B=[h for h in hits if 0xe89a34<=h[0]<0xe8cded]
S=[h for h in hits if 0xe57de0<=h[0]<0xe59000]
for name,ch in (('A',A),('B',B),('S',S)):
    cs=set(h[1] for h in ch)
    print(f'--- chain {name}: {len(ch)} hits, {len(cs)} distinct codes')
    for k,s in CL.items():
        print(f'    {k:<14} inter={len(cs&s):>4} of chain {len(cs&s)/len(cs):>6.1%}  of entity {len(cs&s)/len(s):>6.1%}')
print('A∩B',len(set(h[1] for h in A)&set(h[1] for h in B)))
print('A∩S',len(set(h[1] for h in A)&set(h[1] for h in S)))
print('B∩S',len(set(h[1] for h in B)&set(h[1] for h in S)))
# union coverage of club full 575
cluball=ents['club']
u=set(h[1] for h in A)|set(h[1] for h in B)
print('A∪B ∩ club(all 575) =',len(u&cluball), f'{len(u&cluball)/len(cluball):.1%} of club codes')
notcov=sorted(cluball-u)
print('club codes NOT in A∪B:',len(notcov))
print(notcov[:40])
