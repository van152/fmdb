import re, importlib.util, json
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
spec2 = importlib.util.spec_from_file_location("_b","scratch/t07/out/build.py")
b = importlib.util.module_from_spec(spec2); spec2.loader.exec_module(b)
hits, md = b.decode_cmp_hits(pe); hits.sort()

PARAM={"rdi","rsi","rbx","rcx","rdx","r12","r13","r14","r15","r8","r9"}
SZ={'byte':1,'word':2,'dword':4}
RE_N=re.compile(r"^(mov|movzx|movsx|movsxd|movss|movsd|test|cmp)\s+[a-z0-9]+,\s*(?:(byte|word|dword)\s+ptr\s*)?\[([a-z0-9]+)(?:\s*\+\s*(0x[0-9a-f]+))?\]$")
RE_W=re.compile(r"^(mov)\s+(byte|word|dword)\s+ptr\s*\[([a-z0-9]+)(?:\s*\+\s*(0x[0-9a-f]+))?\]$")

def narrow(ins):
    t=(ins.mnemonic+" "+ins.op_str).lower()
    m=RE_N.match(t)
    if m and m.group(3) in PARAM:
        sz=SZ.get(m.group(2) or 'dword')
        off=int(m.group(4),16) if m.group(4) else 0
        if sz and 0x20<=off<=0x400: return (off,sz,'read')
    m=RE_W.match(t)
    if m and m.group(3) in PARAM:
        off=int(m.group(4),16) if m.group(4) else 0
        if 0x20<=off<=0x400: return (off,SZ[m.group(2)],'write')
    return None

def bfs(t0, span=0x600, maxb=24):
    q=[(t0,0)]; seen=set(); found=[]
    while q and len(seen)<maxb:
        va,d=q.pop(0)
        if va in seen or abs(va-t0)>span: continue
        seen.add(va); fo=pe.va2f(va)
        if fo is None: continue
        for ins in md.disasm(raw[fo:fo+0x100], va):
            a=narrow(ins)
            if a: found.append((d,ins.address,a)); 
            if ins.mnemonic=='ret': break
            if ins.mnemonic=='jmp':
                try: j=int(ins.op_str.strip(),0)
                except ValueError: break
                if abs(j-t0)<=span: q.append((j,d+1))
                break
            if ins.mnemonic in ('je','jz','jne','jnz','jle','jg','jl','jge','ja','jae','jb','jbe','js','jns'):
                try: j=int(ins.op_str.strip(),0)
                except ValueError: break
                if abs(j-t0)<=span: q.append((j,d+1))
                q.append((ins.address+ins.size,d+1))
                break
    found.sort(key=lambda x:(x[0],x[1]))
    return found

def resolve(sub):
    out={}
    for off,code,va,_ in sub:
        ins=list(md.disasm(raw[off:off+0x20],va))
        br=next((x for x in ins[1:4] if x.mnemonic in ('je','jz','jne','jnz')),None)
        if br is None: continue
        if br.mnemonic in ('je','jz'):
            t=int(br.op_str.strip(),0); res=bfs(t)
        else:
            res=bfs(br.address+br.size)
        if res:
            d,addr,a=res[0]
            out.setdefault(code,set()).add((a[0],a[1],a[2]))
    return out
A=[h for h in hits if 0xe82afc<=h[0]<0xe846ac]
B=[h for h in hits if 0xe89a34<=h[0]<0xe8cded]
S=[h for h in hits if 0xe57de0<=h[0]<0xe59000]
for nm,sub in (('A',A),('B',B),('S',S)):
    r=resolve(sub)
    print(nm,len(r),sorted({(c,hex(min(x[0] for x in v))) for c,v in r.items()})[:6])
# calibration
CITY=[('Clat',0x48),('Clon',0x4c),('Cnti',0x20),('Cwea',0x28),('Clgi',0x30),('Clri',0x38)]
chains=[h for h in hits if 0xe54c00<=h[0]<0xe59000]
rc=resolve(chains)
ok=sum(1 for c,o in CITY if c in rc and any(x[0]==o for x in rc[c]))
print('city calibration',ok,'/6')
INJ={'icla':0x4c,'iscl':0x4d,'Imnd':0x34,'Iexd':0x36,'Iiar':0x58,'Irec':0x59,'Iocr':0x30,'Imip':0x50}
