import json, collections, importlib.util, re, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
spec2 = importlib.util.spec_from_file_location("_b","scratch/t07/out/build.py")
b = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(b)
hits, md = b.decode_cmp_hits(pe)
hits.sort()
lo,hi=int(sys.argv[1],16),int(sys.argv[2],16)
sub=[h for h in hits if lo<=h[0]<hi]
si=json.load(open('scratch/t05/schema_inventory.json',encoding='utf-8'))
club={f['code'] for f in si['entities']['club']['fields']}
tail=collections.Counter()
tgt_of={}
for off,code,va,_ in sub:
    ins=list(md.disasm(raw[off:off+0x18],va))
    br=next((x for x in ins[1:4] if x.mnemonic in ("je","jz","jne","jnz")),None)
    if br and br.mnemonic in ("je","jz"):
        tgt_of[code]=int(br.op_str,0)
        tail[int(br.op_str,0)]+=1
print('codes',len(sub),'je codes',len(tgt_of),'distinct je targets',len(tail))
print('top shared targets:',[(hex(k),v) for k,v in tail.most_common(12)])
shared=sum(v for k,v in tail.items() if v>3)
print('codes landing on targets used by >3 codes:',shared, f"{shared/max(1,len(tgt_of)):.1%}")
# for club codes only
clubje={c:t for c,t in tgt_of.items() if c in club}
ct=collections.Counter(clubje.values())
print('club je codes',len(clubje),'distinct targets',len(ct))
print('club top targets:',[(hex(k),v) for k,v in ct.most_common(10)])
