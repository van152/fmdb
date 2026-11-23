import json, collections, importlib.util, re, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
spec2 = importlib.util.spec_from_file_location("_b","scratch/t07/out/build.py")
b = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(b)
hits, md = b.decode_cmp_hits(pe)
hits.sort()
lo,hi=int(sys.argv[1],16),int(sys.argv[2],16)
sub=[h for h in hits if lo<=h[0]<hi]
MEM=re.compile(r"\[(r[a-z0-9]+)(?:\s*\+\s*(0x[0-9a-f]+))?\]")
JMPS=collections.Counter()
first_acc=collections.Counter()
nleaf=0
for off,code,va,_ in sub:
    ins=list(md.disasm(raw[off:off+0x18],va))
    br=None
    for x in ins[1:4]:
        if x.mnemonic in ("je","jz","jne","jnz","jle","jg","jl","jge","ja","jb"):
            br=x; break
    if br is None or br.mnemonic not in ("je","jz"): continue
    nleaf+=1
    t=int(br.op_str,0); tf=pe.va2f(t)
    body=list(md.disasm(raw[tf:tf+0xa0],t))[:24]
    got=None
    for y in body:
        m=MEM.search(y.op_str)
        if m and m.group(1) in ("rdi","rsi","rbx","r12","r13","r14","r15") and y.mnemonic.startswith(("mov","movzx","movsx","movss","lea")):
            got=(m.group(1), m.group(2), y.mnemonic)
            break
    first_acc[got]+=1
    tail=[y for y in body if y.mnemonic=="jmp"]
    for y in tail[:1]: JMPS[y.op_str]+=1
print(f"n={len(sub)} leaves(je)={nleaf}")
print("first member access (reg,off,mn) histogram:")
for k,v in first_acc.most_common(20): print('   ',k,v)
print("first jmp target histogram:")
for k,v in JMPS.most_common(10): print('   ',k,v)
