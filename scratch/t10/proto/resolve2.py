import json, collections, importlib.util, re, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
spec2 = importlib.util.spec_from_file_location("_b","scratch/t07/out/build.py")
b = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(b)
hits, md = b.decode_cmp_hits(pe); hits.sort()
lo,hi=int(sys.argv[1],16),int(sys.argv[2],16)
sub=[h for h in hits if lo<=h[0]<hi]

PARAM={"rdi","rsi","rbx","r12","r13","r14","r15"}
SZ={'byte':1,'word':2,'dword':4}
RE_R=re.compile(r"^(mov|movzx|movsx|movsxd|movss|movsd|lea)\s+([a-z0-9]+),\s*(?:(byte|word|dword|qword)\s*ptr\s*)?\[([a-z0-9]+)(?:\s*\+\s*(0x[0-9a-f]+))?\]$")
JCC={"je","jz","jne","jnz","jle","jg","jl","jge","ja","jae","jb","jbe","js","jns"}

def narrow(body):
    for y in body:
        t=(y.mnemonic+" "+y.op_str).lower()
        m=RE_R.match(t)
        if m and m.group(4) in PARAM:
            disp=int(m.group(5),16) if m.group(5) else 0
            sz=SZ.get(m.group(3) or 'dword')
            if sz and 0x20<=disp<=0x400 and sz in (1,2,4):
                return (disp,sz,y.address,y.mnemonic+" "+y.op_str)
        if y.mnemonic=='ret': break
    return None

def walk(start_va, code, depth=0, seen=None, trail=None):
    """linear walk from start_va; follow jmp into second-level dispatcher on same code."""
    if seen is None: seen=set()
    trail = list(trail or [])
    if start_va in seen or depth>3: return None,[]
    seen.add(start_va)
    fo=pe.va2f(start_va)
    if fo is None: return None,[]
    body=list(md.disasm(raw[fo:fo+0x140],start_va))[:48]
    for k,y in enumerate(body):
        trail.append(f"{y.mnemonic} {y.op_str}")
        r=narrow([y])
        if r: return r,trail
        if y.mnemonic=='ret': return None,trail
        if y.mnemonic=='jmp':
            try: t=int(y.op_str.strip(),0)
            except ValueError: return None,trail
            tf=pe.va2f(t)
            if tf is None: return None,trail
            nxt=list(md.disasm(raw[tf:tf+8],t))[:1]
            # dispatcher detection: compares the code register
            if nxt and nxt[0].mnemonic=='cmp' and nxt[0].op_str.strip().lower().startswith(('r8d','ebx','edx','ecx')):
                return walk_dispatch(t, code, depth+1, seen, trail)
            return walk(t, code, depth+1, seen, trail)
        if y.mnemonic in JCC:
            # take the branch if it is the "match" style; try both
            try: t=int(y.op_str.strip(),0)
            except ValueError: return None,trail
            r,tr=walk(t, code, depth+1, seen, trail+["<take jcc>"])
            if r: return r,tr
            continue
    return None,trail

def walk_dispatch(start_va, code, depth, seen, trail):
    fo=pe.va2f(start_va)
    if fo is None: return None,trail
    body=list(md.disasm(raw[fo:fo+0x900],start_va))
    imm=int.from_bytes(code.encode('latin1'),'little')
    for i,y in enumerate(body):
        if y.mnemonic=='cmp':
            try: v=int(y.op_str.split(',')[1].strip(),0)
            except Exception: continue
            if v!=imm: continue
            for nxt in body[i+1:i+3]:
                if nxt.mnemonic in ('je','jz'):
                    try: t=int(nxt.op_str.strip(),0)
                    except ValueError: continue
                    return walk(t, code, depth+1, seen, trail+[f"disp->{hex(t)}"])
            return None, trail
    return None,trail

got=collections.defaultdict(list)
fail=0
for off,code,va,_ in sub:
    ins=list(md.disasm(raw[off:off+0x18],va))
    br=next((x for x in ins[1:4] if x.mnemonic in ('je','jz')),None)
    if br is None:
        fail+=1; continue
    t=int(br.op_str.strip(),0)
    r,trail=walk(t, code)
    if r: got[code].append((r[0],r[1],hex(r[2])))
    else: fail+=1
print(f"chain {lo:#x}..{hi:#x}: hits={len(sub)} codes={len({h[1] for h in sub})}")
print(f"resolved codes={len(got)}  failed={fail}")
narrow_codes={c:v for c,v in got.items() if v}
print("distinct offsets", len({v[0][0] for v in got.values()}))
multi=[c for c,v in got.items() if len({x[0] for x in v})>1]
print("multi-offset codes", len(multi), multi[:10])
import statistics
offs=sorted({v[0][0] for v in got.values()})
print("min/max", hex(offs[0]), hex(offs[-1]), "n distinct", len(offs))
print("offsets sample", [hex(o) for o in offs[:30]])
Path=lambda p,s: open(p,'w',encoding='utf-8').write(s)
Path('scratch/t10/proto/resolved.json', json.dumps({c:v for c,v in got.items()}, ensure_ascii=False, indent=1))
