import json, collections, importlib.util, re, sys
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
lo,hi=int(sys.argv[1],16),int(sys.argv[2],16)
start=lo; end=hi
va=pe.f2va(start)
ins=list(md.disasm(raw[lo:hi],va))
print('insns',len(ins))
# collect cmp r8d, imm ; je <tgt>
codes={}
for i,x in enumerate(ins):
    if x.mnemonic=='cmp' and x.op_str.startswith('r8d'):
        try: imm=int(x.op_str.split(',')[1].strip(),0)
        except Exception: continue
        code=imm.to_bytes(4,'little')[::-1].decode('latin1')
        nxt=ins[i+1] if i+1<len(ins) else None
        tgt=None
        if nxt and nxt.mnemonic in ('je','jz','jne','jnz'):
            try: tgt=int(nxt.op_str,0)
            except ValueError: pass
        codes.setdefault(code,[]).append((x.address,nxt.mnemonic if nxt else None, tgt))
print('codes in dispatcher',len(codes))
offs=collections.Counter()
for code,ent in codes.items():
    for addr,mn,tgt in ent:
        if tgt is None or mn not in ('je','jz'): continue
        tf=pe.va2f(tgt)
        body=list(md.disasm(raw[tf:tf+0xc0],tgt))[:30]
        found=None
        for y in body:
            m=re.search(r"\[(rdi|rsi|rbx|r12|r13|r14|r15)(?:\s*\+\s*(0x[0-9a-f]+))?\]", y.op_str)
            if m and y.mnemonic.startswith(('mov','movzx','movsx','movss','lea')) and not y.op_str.startswith('['):
                disp=int(m.group(2),16) if m.group(2) else 0
                found=(disp, y.mnemonic)
                break
            if y.mnemonic=='ret': break
        if found: offs[(code,)+found]+=1
print('leaves with member access',len(offs))
for k,v in list(offs.items())[:40]: print('  ',k)
