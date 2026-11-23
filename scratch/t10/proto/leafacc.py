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
PARAM={"r12","r13","rbx","rdi","rsi","r14","r15","rcx","rdx","r8","r9"}
RE_R=re.compile(r"^(?:mov|movzx|movsx|movsxd|movss|movsd|lea)\s+[a-z0-9]+,\s*(?:(byte|word|dword|qword)\s*ptr\s*)?\[([a-z0-9]+)(?:\s*\+\s*(0x[0-9a-f]+))?\]$")
got={}
miss=collections.Counter()
for off,code,va,_ in sub:
    ins=list(md.disasm(raw[off:off+0x18],va))
    br=None
    for x in ins[1:4]:
        if x.mnemonic in ("je","jz"): br=x; break
    if br is None: continue
    t=int(br.op_str,0); tf=pe.va2f(t)
    body=list(md.disasm(raw[tf:tf+0x120],t))[:40]
    found=None
    for y in body:
        txt=(y.mnemonic+" "+y.op_str).lower()
        m=RE_R.match(txt)
        if m and m.group(2) in PARAM:
            disp=int(m.group(3),16) if m.group(3) else 0
            if 0x20<=disp<=0x400:
                found=(disp, {'byte':1,'word':2,'dword':4,'qword':8}.get(m.group(1) or 'dword',4), y.mnemonic, hex(y.address))
                break
        if y.mnemonic=='ret': break
    if found: got.setdefault(code,[]).append(found)
    else: miss[code]+=1
print(f"cluster {lo:#x}..{hi:#x}: hits={len(sub)} codes={len({h[1] for h in sub})}")
print(f"codes with offset: {len(got)}")
multi={c:v for c,v in got.items() if len({x[0] for x in v})>1}
print(f"codes with >1 distinct offset: {len(multi)}")
for c,v in list(got.items())[:15]: print('  ',c,v[0])
