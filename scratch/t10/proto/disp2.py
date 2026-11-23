import json, collections, importlib.util, re, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
start=int(sys.argv[1],16); span=int(sys.argv[2],16) if len(sys.argv)>2 else 0x1000
va=pe.f2va(start)
body=list(md.disasm(raw[start:start+span],va))
print('insns',len(body))
pairs=[]
for i,y in enumerate(body):
    if y.mnemonic!='cmp': continue
    part=y.op_str.split(',')
    if len(part)!=2 or part[0].strip() not in ('r8d','ebx','edx','ecx','r9d'): continue
    try: v=int(part[1].strip(),0)
    except Exception: continue
    if not (0x20202020<=v<=0x7e7e7e7e): continue
    bs=v.to_bytes(4,'big')
    if not all(48<=c<=57 or 65<=c<=90 or 97<=c<=122 for c in bs): continue
    code=bs.decode('latin1')
    nxt=[x for x in body[i+1:i+3]]
    if nxt and nxt[0].mnemonic in ('je','jz'):
        pairs.append((code, nxt[0].op_str, hex(y.address)))
print('code cmps',len(pairs),'distinct',len({p[0] for p in pairs}))
acc=collections.Counter()
for code,tgt,addr in pairs[:200]:
    t=int(tgt,0)
    print(code, tgt)
