import json, collections
from pathlib import Path
from capstone import Cs, CS_ARCH_X86, CS_MODE_64
import importlib.util, re
spec = importlib.util.spec_from_file_location("_pe","scripts/t05_pe.py")
pm = importlib.util.module_from_spec(spec); spec.loader.exec_module(pm)
pe=pm.default(); raw=pe.raw
md=Cs(CS_ARCH_X86, CS_MODE_64)
hits=json.loads(Path("scratch/t10/proto/hits.json").read_text()); hits.sort()
byoff={o:c for o,c in hits}; offs=set(byoff)
JCC={"je","jz","jne","jnz","jle","jg","jl","jge","ja","jae","jb","jbe","js","jns","jo","jno","jp","jnp"}
# examine one leaf of chain A
for start in (0xe82afc,0xe82b04):
    va=pe.f2va(start)
    print('---',hex(start))
    for i in list(md.disasm(raw[start:start+0x30], va))[:8]:
        print('   ',hex(i.address),i.mnemonic,i.op_str)
# follow je of a leaf cmp e.g. 0xe834a5 -> 0x140e83bc5
for off in (0xe834a5,):
    va=pe.f2va(off)
    ins=list(md.disasm(raw[off:off+0x14],va))
    for x in ins[:3]:
        print('cmp@',hex(off),x.mnemonic,x.op_str)
        if x.mnemonic in ("je","jz"):
            t=int(x.op_str,0); tf=pe.va2f(t)
            print('   target file',hex(tf))
            for y in md.disasm(raw[tf:tf+0x40], t):
                print('      ',hex(y.address),y.mnemonic,y.op_str)
                if y.mnemonic=='ret': break
